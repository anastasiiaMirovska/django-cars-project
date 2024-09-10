from django.db import models


class TransmissionTypeChoices(models.TextChoices):
    Manual = 'Manual'
    Automatic = 'Automatic'