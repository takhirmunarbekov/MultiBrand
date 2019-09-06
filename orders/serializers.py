from rest_framework import serializers

from goods.serializers import (
    ItemSerializer,
)

from .models import (
    ItemOrder,
    Order,
)


class ItemOrderReadOnlySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    item = ItemSerializer(read_only=True)

    class Meta:

        model = ItemOrder
        fields = (
            'id',
            'item',
            'vendor_code',
            'name',
            'amount',
            'unit',
            'price',
            'price_currency',
        )
        read_only_fields = (
            'id',
            'item',
            'vendor_code',
            'name',
            'amount',
            'unit',
            'price',
            'price_currency',
        )


class ItemOrderSerializer(serializers.ModelSerializer):

    class Meta:

        model = ItemOrder
        fields = (
            'item',
            'vendor_code',
            'name',
            'amount',
            'unit',
            'price',
            'price_currency',
        )
        read_only_fields = (
            'vendor_code',
            'name',
            'unit',
            'price',
            'price_currency',
        )
        extra_kwargs = {
            'item': {
                'required': True
            }
        }
    

class ItemOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:

        model = ItemOrder
        fields = (
            'item',
            'vendor_code',
            'name',
            'amount',
            'unit',
            'price',
            'price_currency',
        )
        read_only_fields = (
            'item',
            'vendor_code',
            'name',
            'unit',
            'price',
            'price_currency',
        )


class OrderSerializer(serializers.ModelSerializer):

    class Meta:

        model = Order
        fields = (
            'city',
            'region',
            'address',
            'phone_number',
            'email',
            'comment',
        )


class BillSerializer(serializers.Serializer):

    cost = serializers.CharField()
    cost_currency = serializers.CharField()


class BasketItemOrderSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    cost = serializers.CharField()
    cost_currency = serializers.CharField()

    class Meta:

        model = ItemOrder
        fields = (
            'id',
            'name',
            'amount',
            'unit',
            'cost',
            'cost_currency',
        )


class BasketOrderSerializer(serializers.Serializer):

    order = OrderSerializer()
    items = BasketItemOrderSerializer(many=True, read_only=True)
    bill = BillSerializer(read_only=True)
    

class ConfirmOrderSerializer(serializers.Serializer):

    transaction_id = serializers.IntegerField(required=False)
    payment = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES)

    def validate(self, data):
        if data['payment'] == 'card' and 'transaction_id' not in data:
            raise serializers.ValidationError({
                'transaction_id': ["This field is required."]})
        return data


class CryptogramSerializer(serializers.Serializer):

    cardholder_name = serializers.CharField()
    cryptogram = serializers.CharField()


class SecureThreeDsSerializer(serializers.Serializer):

    transaction_id = serializers.IntegerField()
    pa_req = serializers.CharField()
    acs_url = serializers.URLField()


class SecureThreeDsConfirmationSerializer(serializers.Serializer):

    transaction_id = serializers.IntegerField()
    pa_res = serializers.CharField()


class PaymentConfirmationSerializer(serializers.Serializer):

    transaction_id = serializers.IntegerField()


class CloudPaymentsErrorSerializer(serializers.Serializer):

    response = serializers.JSONField()
    # message = serializers.CharField()


class PaymentErrorSerializer(serializers.Serializer):

    transaction_id = serializers.IntegerField()
    reason = serializers.CharField()
    # reason_code = serializers.IntegerField()
    cardholder_message = serializers.CharField()


class TransactionSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    amount = serializers.FloatField()
    currency = serializers.CharField()
    # currency_code = serializers.IntegerField()
    # invoice_id = serializers.CharField()
    account_id = serializers.CharField()
    email = serializers.EmailField()
    description = serializers.CharField()
    # data = serializers.JSONField()
    created_date = serializers.DateTimeField()
    auth_date = serializers.DateTimeField()
    confirm_date = serializers.DateTimeField()
    auth_code = serializers.CharField()
    test_mode = serializers.BooleanField()
    ip_address = serializers.IPAddressField()
    # ip_country = serializers.CharField()
    # ip_city = serializers.CharField()
    # ip_region = serializers.CharField()
    # ip_district = serializers.CharField()
    # ip_latitude = serializers.FloatField()
    # ip_longitude = serializers.FloatField()
    card_first_six = serializers.CharField()
    card_last_four = serializers.CharField()
    card_exp_date = serializers.CharField()
    card_type = serializers.CharField()
    # card_type_code = serializers.IntegerField()
    issuer = serializers.CharField()
    issuer_bank_country = serializers.CharField()
    status = serializers.CharField()
    # status_code = serializers.IntegerField()
    reason = serializers.CharField()
    # reason_code = serializers.IntegerField()
    cardholder_message = serializers.CharField()
    name = serializers.CharField()
    # token = serializers.CharField()