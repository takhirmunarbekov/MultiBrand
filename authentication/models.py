from django.db import models

# Create your models here.



from uuid import uuid4

from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class BaseModel(models.Model):

    created = models.DateTimeField(verbose_name=_("Created"),
                                   auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Updated"),
                                   auto_now=True)

    class Meta:
        
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, phone_number, first_name,
                    last_name, email, password,
                    **extra_fields):
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone_number, first_name,
                         last_name, email, password,
                         **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        user = self.create_user(phone_number, first_name, last_name,
                                email, password, **extra_fields)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):

    username = None
    email = models.EmailField(verbose_name=_("Email"),
                              unique=True)
    first_name = models.CharField(_('First name'), max_length=30)
    last_name = models.CharField(_('Last name'), max_length=150)
    phone_number = PhoneNumberField(verbose_name=_("Phone number"),
                                    unique=True)
    avatar = models.ImageField(
        verbose_name=_("Avatar"),
        upload_to='avatars/%Y/%m/%d',
        blank=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    objects = UserManager()
    
    class Meta:

        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name