# Generated by Django 5.1 on 2024-09-08 11:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='carmodelmodel',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='cars.carbrandmodel'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='cars.carmodelmodel'),
        ),
        migrations.AddField(
            model_name='carprofilemodel',
            name='car',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='cars.carmodel'),
        ),
        migrations.AlterUniqueTogether(
            name='carmodelmodel',
            unique_together={('name', 'brand')},
        ),
    ]
