from django.core import validators as V
from django.db import models

from core.enums.regex_enums import RegexEnum
from core.models import BaseModel


class AutoParkModel(BaseModel):
    class Meta:
        db_table = 'auto_parks'
        ordering = ('id',)

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, validators=[V.RegexValidator(*RegexEnum.PHONE.value)])
    description = models.CharField(max_length=255)

    main_user = models.ForeignKey('users.UserModel', on_delete=models.CASCADE, related_name='auto_parks')
