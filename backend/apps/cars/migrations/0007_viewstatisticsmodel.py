# Generated by Django 5.1.1 on 2024-09-11 00:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_remove_carmodel_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewStatisticsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='cars.carmodel')),
            ],
            options={
                'db_table': 'views',
                'ordering': ('id',),
            },
        ),
    ]
