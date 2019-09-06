from rest_framework import serializers

from rest_framework_recursive.fields import RecursiveField

from .models import (
    Category,
    Item,
    Feedback,
    Rating,
    Stock,
)


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:

        model = Feedback
        fields = (
            'id',
            'text',
            'user',
        )
        read_only_fields = (
            'user',
        )


class RatingSerializer(serializers.ModelSerializer):

    class Meta:

        model = Rating
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):

    class Meta:

        model = Stock
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    of = RecursiveField()

    class Meta:

        model = Category
        fields = (
            'id',
            'of',
            'name',
            'description',
        )


class CategoryNoneRecursiveSerializer(serializers.ModelSerializer):

    class Meta:

        model = Category
        fields = (
            'id',
            'subcategories',
            'name',
            'description',
        )


class CategoriesJsonSerializer(serializers.Serializer):

    categories = serializers.ListField(
        child=serializers.JSONField()
    )


class ItemSerializer(serializers.ModelSerializer):

    stock = StockSerializer()
    liked = serializers.IntegerField(
        source='likes.count', 
        read_only=True
    )
    rating = serializers.FloatField(
        read_only=True
    )
    is_liked = serializers.BooleanField(
        read_only=True
    )
    is_rated = serializers.BooleanField(
        read_only=True
    )

    class Meta:

        model = Item
        fields = (
            'id',
            'name',
            'desc',
            'amount',
            'unit',
            'image',
            'price_currency',
            'price',
            'is_new',
            'is_hit',
            'stock',
            'liked',
            'rating',
            'is_hit',
            'is_new',
            'is_popular',
            'is_liked',
            'is_rated',
        )


class ItemDetailSerializer(ItemSerializer):

    category = CategorySerializer()

    class Meta(ItemSerializer.Meta):

        fields = ItemSerializer.Meta.fields + (
            'body',
            'description',
            'category',
        )


class CheckableSerializer(serializers.Serializer):

    is_set = serializers.BooleanField()