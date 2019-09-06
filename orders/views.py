from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money

from goods.models import (
    Item,
)

from .serializers import (
    ItemOrderReadOnlySerializer,
    ItemOrderSerializer,
    ItemOrderDetailSerializer,
    BasketOrderSerializer,
    ConfirmOrderSerializer,

    CryptogramSerializer,
    SecureThreeDsSerializer,
    SecureThreeDsConfirmationSerializer,
    PaymentConfirmationSerializer,
    TransactionSerializer,
    CloudPaymentsErrorSerializer,
)

from .paginations import (
    ItemOrdersSetPagination,
)

from collections import defaultdict

from django.core.cache import caches

from cryptography.fernet import Fernet
from uuid import uuid4
import json

from django.urls import reverse

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from cloudpayments import CloudPayments
from cloudpayments.models import (
    Secure3d,
    Transaction,
)

from cloudpayments.errors import (
    CloudPaymentsError,
    PaymentError,
)

from django.conf import settings


# Create your views here.

BASKET_KEY = 'basket'
ORDER_KEY = 'order'
DEFAULT_CURRENCY = 'KZT'
DEFAULT_TIMEOUT = 3 * 24 * 60 * 60 + 3600


class OrderManager:

    @staticmethod
    def from_data(data):
        try:
            orders_cache = caches['orders']
            data_cache = caches['data']
            key = data_cache.get(data).encode()
            fernet = Fernet(key)
            data = json.loads(fernet.decrypt(data.encode()).decode())
            values = orders_cache.get(data['uuid'])
            return key, OrderManager(
                order=values['order'],
                items=values['items'],
                deadline=values['deadline'],
                order_id=values['order_id'],
            )
        except AttributeError:
            raise NotFound()

    def __init__(self, order, items,
            deadline=None, order_id=None):
        self.order = order
        self.items = items
        self.deadline = deadline
        self.order_id = order_id

    def save(self, uuid, data, key):
        orders_cache = caches['orders']
        data_cache = caches['data']
        self.deadline = timezone.now() + timezone.timedelta(
            seconds=DEFAULT_TIMEOUT)
        orders_cache.set(uuid, {
            'order': self.order,
            'items': self.items,
            'deadline': self.deadline,
            'order_id': self.order_id,
        }, DEFAULT_TIMEOUT)
        data_cache.set(data, key, DEFAULT_TIMEOUT)

    def pack(self, uuid):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        data = fernet.encrypt(json.dumps({
            'uuid': uuid,
        }).encode()).decode()
        self.save(uuid, data, key.decode())
        return data


class ConfirmOrderAPIView(APIView):

    def get(self, request, data):
        key, order_manager = OrderManager.from_data(data)
        if order_manager.order_id is None:
            return Response({
                'order': order_manager.order,
                'items': order_manager.items,
                'deadline': order_manager.deadline,
            })
        else:
            return Response({
                'order_id': order_manager.order_id,
            })

    def post(self, request, data):
        serializer = ConfirmOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['payment'] == 'card':
            client = CloudPayments(
                settings.CLOUDPAYMENTS['public_id'],
                settings.CLOUDPAYMENTS['api_secret']
            )
            try:
                transaction = client.get_transaction(serializer.validated_data['transaction_id'])
                serializer = TransactionSerializer(transaction)
                
                # Fail: client.refund(serializer.data['id'], serializer.data['amount'])

                # Confirm: client.confirm_payment(
                #     serializer.validated_data['transaction_id'],
                #     100000
                # )

                key, order_manager = OrderManager.from_data(data)

                return Response(serializer.data, status=status.HTTP_200_OK)
            except (PaymentError, CloudPaymentsError) as error:
                serializer = CloudPaymentsErrorSerializer(error) \
                    if isinstance(error, CloudPaymentsError) else PaymentError(error)
                return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        elif serializer.validated_data['payment'] == 'in cash':
            pass
        
        else:

            return Response(status.HTTP_404_NOT_FOUND)


class OrderAPIView(APIView):

    def get(self, request):
        item_orders = request.session.get(BASKET_KEY, {})
        bill_items = []
        total = Money('0', DEFAULT_CURRENCY)
        for item, item_order in item_orders.items():
            cost = convert_money(Money(item_order['price'],
                item_order['price_currency']) * item_order['amount'], DEFAULT_CURRENCY)
            bill_items.append({
                'id': item,
                'name': item_order['name'],
                'amount': item_order['amount'],
                'unit': item_order['unit'],
                'cost': cost.amount,
                'cost_currency': cost.currency,
            })
            total += cost
        serializer = BasketOrderSerializer({
            'order': request.session.get(ORDER_KEY, defaultdict(lambda: None)),
            'bill': { 'cost': total.amount, 'cost_currency': total.currency },
            'items': bill_items,
        })
        return Response(serializer.data)

    def put(self, request):
        serializer = BasketOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.session[ORDER_KEY] = serializer.validated_data['order']
        request.session.modified = True
        return Response(serializer.data)

    def post(self, request):
        try:
            items = request.session.get(BASKET_KEY)
            order = request.session.get(ORDER_KEY)
            order_manager = OrderManager(order, items)
            data = order_manager.pack(uuid4().hex)
            # TODO: Send email
            return Response({
                'url': request.build_absolute_uri(
                    reverse('confirm_order', kwargs={'data': data}))
            })
        except AttributeError:
            raise NotFound()


class BasketAPIView(APIView):

    pagination_class = ItemOrdersSetPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
         if self.paginator is None:
             return None
         return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
         assert self.paginator is not None
         return self.paginator.get_paginated_response(data)

    def get(self, request):
        item_orders = request.session.get(BASKET_KEY, {}).copy()
        items = Item.objects.filter(id__in=item_orders.keys())
        for item in items:
            item_orders[str(item.pk)]['item'] = item
        for item, item_order in item_orders.items():
            item_order['id'] = item
            if type(item_order['item']) is not Item:
                item_order['item'] = None
        page = self.paginate_queryset(list(item_orders.values()))
        if page is not None:
            serializer = ItemOrderReadOnlySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ItemOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data['item']
        amount = serializer.validated_data['amount']
        price = convert_money(Money(item.price.amount, item.price.currency), DEFAULT_CURRENCY)
        serializer = ItemOrderSerializer({
            'item': item,
            'vendor_code': item.vendor_code,
            'name': item.name,
            'amount': amount,
            'unit': item.unit,
            'price': price.amount,
            'price_currency': price.currency,
        })
        items = request.session.get(BASKET_KEY, {})
        items[str(serializer.data['item'])] = serializer.data
        request.session[BASKET_KEY] = items
        request.session.modified = True
        item_order = items[str(item.pk)].copy()
        item_order['item'] = item
        serializer = ItemOrderReadOnlySerializer(item_order)
        return Response(serializer.data)

    def delete(self, request):
        request.session[BASKET_KEY] = {}
        request.session.modified = True
        return Response(status=status.HTTP_204_NO_CONTENT)


class BasketDetailAPIView(APIView):

    def get(self, request, pk):
        items = request.session.get(BASKET_KEY, {})
        if str(pk) not in items:
            raise NotFound("Order item not found.")
        item_order = items[str(pk)].copy()
        item_order['id'] = item_order['item']
        try:
            item = Item.objects.get(pk=pk)
            item_order['item'] = item
        except Item.DoesNotExist:
            item_order['item'] = None
        serializer = ItemOrderReadOnlySerializer(item_order)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = ItemOrderDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        items = request.session.get(BASKET_KEY, {})
        if str(pk) not in items:
            raise NotFound("Order item not found.")
        items[str(pk)]['amount'] = amount
        request.session[BASKET_KEY] = items
        request.session.modified = True
        item_order = items[str(pk)].copy()
        item_order['id'] = item_order['item']
        try:
            item = Item.objects.get(pk=pk)
            item_order['item'] = item
        except Item.DoesNotExist:
            item_order['item'] = None
        serializer = ItemOrderReadOnlySerializer(item_order)
        return Response(serializer.data)

    def delete(self, request, pk):
        items = request.session.get(BASKET_KEY, {})
        items.pop(str(pk), None)
        request.session[BASKET_KEY] = items
        request.session.modified = True
        return Response(status=status.HTTP_204_NO_CONTENT)