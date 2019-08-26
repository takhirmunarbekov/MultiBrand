from django.contrib import admin
from .models import (
    Category,
    Item,
    Stock,
    Feedback,
    Rating,
    Like
)


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'vendor_code',
        'description',
        'created',
        'updated',
        'price',
    )
    list_filter = (
        'category',
    )
    ordering = ('category', 'name', 'vendor_code', 'price',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):

    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):

    pass