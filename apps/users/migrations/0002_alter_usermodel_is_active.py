# Generated by Django 5.1 on 2024-09-07 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
