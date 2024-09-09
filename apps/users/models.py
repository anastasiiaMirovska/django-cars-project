from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators as V
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.enums.regex_enums import RegexEnum
from core.models import BaseModel

from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ('id',)

    email = models.EmailField(unique=True)
    password = models.CharField(_("password"), max_length=128, validators=[V.RegexValidator(*RegexEnum.PASSWORD.value)])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()


class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'
        ordering = ('id',)

    name = models.CharField(max_length=20, validators=[V.RegexValidator(*RegexEnum.NAME.value)])
    surname = models.CharField(max_length=20)
    age = models.IntegerField()
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=13, validators=[V.RegexValidator(*RegexEnum.PHONE.value)])
