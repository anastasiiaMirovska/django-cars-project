from django.db import models


class BodyTypeChoices(models.TextChoices):
    HatchBack = 'HatchBack'
    Sedan = 'Sedan',
    Coupe = 'Coupe',
    Wagon = 'Wagon',
    Jeep = 'Jeep',
    Minivan = 'Minivan',
    LiftBack = 'LiftBack',
    MicroVan = 'MicroVan',
    Pickup = 'PickUp',
    Roadster = 'Roadster',
    Cabriolet = 'Cabriolet',
    Limousine = 'Limousine',
    FastBack = 'FastBack'

