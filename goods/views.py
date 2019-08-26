from django.shortcuts import get_object_or_404
from django.db.models import (
    Count, Case, When, BooleanField, FloatField, Avg, F
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import (
    Category,
    Item,
    Feedback,
    Like,
    Rating,
)

from .serializers import (
    ItemSerializer,
    ItemDetailSerializer,
    FeedbackSerializer,
    CheckableSerializer,
)

from .paginations import (
    ItemsSetPagination,
)


# Create your views here.

class ItemsViewSet(ReadOnlyModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemsSetPagination

    def get_queryset(self):
        likes = ratings = []
        if not self.request.user.is_anonymous:
            likes = self.request.user.likes.values_list('item')
            ratings = self.request.user.ratings.values_list('item')
        queryset = self.queryset.annotate(
            rating=Avg('ratings__rate')
        ).annotate(
            rating=Case(
                When(rating=None, then=0),
                default=F('rating'),
                output_field=FloatField()
            ),
            is_liked=Case(
                When(id__in=likes, then=True),
                default=False,
                output_field=FloatField()
            ),
            is_rated=Case(
                When(id__in=ratings, then=True),
                default=False,
                output_field=FloatField()
            )
        )
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ItemDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=['POST'],
        permission_classes=[IsAuthenticated],
        serializer_class=CheckableSerializer)
    def like(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = get_object_or_404(self.get_queryset(), pk=pk)
        if serializer.validated_data['is_set']:
            item.likes.get_or_create(item=pk, user=request.user)
        else:
            item.likes.filter(item=pk, user=request.user).delete()
        return Response(serializer.data)

    @action(detail=True, methods=['POST'],
        permission_classes=[IsAuthenticated],
        serializer_class=CheckableSerializer)
    def rate(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = get_object_or_404(self.get_queryset(), pk=pk)
        if serializer.validated_data['is_set']:
            item.ratings.get_or_create(item=pk, user=request.user)
        else:
            item.ratings.filter(item=pk, user=request.user).delete()
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'POST'],
        permission_classes=[IsAuthenticated],
        serializer_class=FeedbackSerializer)
    def feedbacks(self, request, pk):
        if request.method == 'GET':
            queryset = Feedback.objects.filter(item=pk)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            item = get_object_or_404(self.get_queryset(), pk=pk)
            feedback = item.feedbacks.create(user=request.user,
                **serializer.validated_data)
            return Response(self.serializer_class(feedback).data)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class CategorizedItemsViewSet(ListAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemsSetPagination

    def get_queryset(self):
        likes = ratings = []
        if not self.request.user.is_anonymous:
            likes = self.request.user.likes.values_list('item')
            ratings = self.request.user.ratings.values_list('item')
        queryset = self.queryset.annotate(
            rating=Avg('ratings__rate')
        ).annotate(
            rating=Case(
                When(rating=None, then=0),
                default=F('rating'),
                output_field=FloatField()
            ),
            is_liked=Case(
                When(id__in=likes, then=True),
                default=False,
                output_field=FloatField()
            ),
            is_rated=Case(
                When(id__in=ratings, then=True),
                default=False,
                output_field=FloatField()
            )
        )
        return queryset

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
        return self.paginator.paginate_queryset(queryset,
            self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def list(self, request, category):
        try:
            if category == 'all':
                queryset = self.get_queryset()
            else:
                queryset = self.get_queryset() \
                    .filter(category=int(category))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response(status=status.HTTP_404_NOT_FOUND)


class HitItemsViewSet(CategorizedItemsViewSet):

    queryset = Item.objects.filter(is_hit=True)


class NewItemsViewSet(CategorizedItemsViewSet):

    queryset = Item.objects.filter(is_new=True)


class PopularItemsViewSet(CategorizedItemsViewSet):

    queryset = Item.objects.filter(is_popular=True)
