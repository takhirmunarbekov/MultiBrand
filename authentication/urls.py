from django.urls import path, re_path, include
from django.views.generic import TemplateView, RedirectView

from rest_framework.routers import SimpleRouter

from allauth.account.views import PasswordResetView

from rest_auth.registration.views import VerifyEmailView, RegisterView

from .views import (
    UserViewSet,
    EmailAddressViewSet,
)


router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('register/', include('rest_auth.registration.urls')),
    path('verify/',
        VerifyEmailView.as_view(),
        name='account_email_verification_sent'),
    path('verify/<str:key>/',
        TemplateView.as_view(template_name="authentication/verify.html"),
        name='account_confirm_email'),
    path('reset/<str:uidb64>:<str:token>/',
        TemplateView.as_view(template_name="authentication/reset.html"),
        name='password_reset_confirm'),
    path('email/', include([
        path('', EmailAddressViewSet.as_view({
            'post': 'check',
        })),
        path('send/', EmailAddressViewSet.as_view({
            'post': 'send_verification_link',
        }))
    ])),
] + router.urls