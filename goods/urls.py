from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import (
    CategoriesViewSet,
    ItemsViewSet,
    CategorizedItemsViewSet,
    HitItemsViewSet,
    NewItemsViewSet,
    PopularItemsViewSet,
)


router = SimpleRouter()
router.register('categories', CategoriesViewSet)
router.register('', ItemsViewSet)


urlpatterns = [
    path('category/<str:category>/', include([
        path('', CategorizedItemsViewSet.as_view()),
        path('hit/', HitItemsViewSet.as_view()),
        path('new/', NewItemsViewSet.as_view()),
        path('popular/', PopularItemsViewSet.as_view()),
    ])),
] + router.urls
