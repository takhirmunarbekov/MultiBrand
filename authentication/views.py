import json
import requests

from uuid import uuid4
from datetime import datetime
from datetime import timedelta

from django.db import transaction
from django.core.cache import caches
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.utils.translation import ugettext as _

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from allauth.account.models import EmailAddress
from allauth.account.utils import (
    setup_user_email,
    send_email_confirmation,
)

from .models import CustomUser as UserModel

from .serializers import (
    UserSerializer,
    EmailAddressSerializer,
    EmailSerializer,
)


# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PUT'])
    def overwrite_mine(self, request):
        serializer = self.serializer_class(
            request.user,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PATCH'])
    def change_mine(self, request):
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailAddressViewSet(viewsets.ViewSet):

    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer
    permission_classes = (AllowAny,)

    def get_email_address(self, request, user):
        try:
            return EmailAddress.objects.get(email=user.email)
        except ObjectDoesNotExist:
            setup_user_email(request, user, [])
            send_email_confirmation(request, user)
            return EmailAddress.objects.get(email=user.email)

    @action(detail=False, methods=['POST'])
    def check(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, email=serializer.validated_data['email'])
        serializer = self.serializer_class(self.get_email_address(request, user))
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], serializer_class=EmailSerializer)
    def send_verification_link(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, email=serializer.validated_data['email'])
        email_address = self.get_email_address(request, user)
        email_address.send_confirmation(request)
        return Response(serializer.data, status=status.HTTP_200_OK)