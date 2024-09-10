from django.db import models


class EngineTypeChoices(models.TextChoices):
    PetrolEngine = 'PetrolEngine'
    DieselEngine = 'DieselEngine'
    ElectricMotor = 'ElectricMotor'
