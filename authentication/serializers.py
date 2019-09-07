import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework import serializers, exceptions
from rest_framework.utils.representation import smart_repr

from allauth.account import app_settings as allauth_settings
from allauth.account.utils import (
    setup_user_email,
    send_email_confirmation,
)
from allauth.account.adapter import get_adapter
from allauth.utils import (
    email_address_exists,
)
from allauth.account.models import EmailAddress

from rest_auth.models import TokenModel

from phonenumber_field.serializerfields import PhoneNumberField



# Get the UserModel
UserModel = get_user_model()


class NotBlankValidator(object):

    missing_message = _("This field is not allowed to be blank.")

    def __init__(self, fields):
        self.fields = fields

    def enforce_required_fields(self, attrs):
        missing = dict([
            (field_name, self.missing_message)
            for field_name in self.fields
            if field_name in attrs and not bool(attrs[field_name])
        ])
        if missing:
            raise exceptions.ValidationError(missing)

    def __call__(self, attrs):
        self.enforce_required_fields(attrs)

    def __repr__(self):
        return '<%s(fields=%s)>' % (
            self.__class__.__name__,
            smart_repr(self.fields)
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'avatar',
        )
        read_only_fields=(
            'email',
        )
        extra_kwargs={
            'first_name': {
                'required': True,
                'allow_null': False
            },
            'last_name': {
                'required': True,
                'allow_null': False
            },
            'phone_number': {
                'required': True,
                'allow_null': False
            },
        }
        validators = [
            NotBlankValidator(
                fields=(
                    'first_name',
                    'last_name',
                    'phone_number',
                )
            )
        ]


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(style={
        'input_type': 'password',
        'placeholder': _("Password"),
    })

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = None
        if 'allauth' in settings.INSTALLED_APPS:
            if allauth_settings.AUTHENTICATION_METHOD == allauth_settings.AuthenticationMethod.EMAIL:
                user = self.authenticate(email=email, password=password)
        else:
            try:
                email = UserModel.objects.get(email__iexact=email).get_email()
                user = self.authenticate(email=email, password=password)
            except UserModel.DoesNotExist:
                pass
        if user:
            if not user.is_active:
                raise exceptions.ValidationError(_("User account is disabled."))
        else:
            raise exceptions.ValidationError(_("Unable to log in with provided credentials."))
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
                try:
                    email_address = user.emailaddress_set.get(email=user.email)
                except ObjectDoesNotExist:
                    setup_user_email(self.context['request'], user, [])
                    send_email_confirmation(self.context['request'], user)
                    raise serializers.ValidationError(_("Verification e-mail sent."))
                if not email_address.verified:
                    raise serializers.ValidationError(_("Email is not verified."))
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED,
        style={
            'placeholder': _("Email"),
        })
    phone_number = PhoneNumberField(
        style={
            'placeholder': _("Phone number"),
        }
    )
    first_name = serializers.CharField(max_length=30,
        style={
            'placeholder': _("First name"),
        })
    last_name = serializers.CharField(max_length=150,
        style={
            'placeholder': _("Last name"),
        })
    password = serializers.CharField(write_only=True,
        style={
            'input_type': 'password',
            'placeholder': _("Password"),
        })
    confirm_password = serializers.CharField(write_only=True,
        style={
            'input_type': 'password',
            'placeholder': _("Confirm password"),
        })

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this email address."))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate_confirm_password(self, password):
        if password != self.initial_data['password']:
            raise serializers.ValidationError(_("Passwords don't match."))
        return password

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user


class TokenSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user',)


class EmailAddressSerializer(serializers.Serializer):

    email = serializers.EmailField()
    verified = serializers.BooleanField(read_only=True)


class EmailSerializer(serializers.Serializer):

    email = serializers.EmailField()