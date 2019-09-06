from django.contrib import admin

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    CustomUser,
)

from .forms import (
    UserCreationForm
)


# Register your models here.

class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            )
        }),
        (_('Personal info'), {
            'fields': (
                'phone_number',
                'first_name',
                'last_name',
                'avatar',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        (_('Important dates'), {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'phone_number',
                'password1',
                'password2',
            ),
        }),
    )
    list_display = (
        'email',
        'first_name',
        'last_name', 
        'phone_number',
        'is_staff',
        'last_login',
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'phone_number',
    )
    ordering = ('email',)

admin.site.register(CustomUser, UserAdmin)