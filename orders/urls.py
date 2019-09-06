from django.urls import path, include

from .views import (
    BasketAPIView,
    BasketDetailAPIView,
    OrderAPIView,
    ConfirmOrderAPIView,
)



urlpatterns = [
    path('basket/', BasketAPIView.as_view()),
    path('basket/<int:pk>/', BasketDetailAPIView.as_view()),
    path('basket/order/', OrderAPIView.as_view()),
    path('<str:data>/', ConfirmOrderAPIView.as_view(), name='confirm_order'),
]
