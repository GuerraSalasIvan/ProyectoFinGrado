# Generated by Django 4.2.8 on 2024-01-24 12:28

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_promocion_descripcion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocion',
            name='fecha_fin_promocion',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2024, 1, 24, 12, 28, 33, 842801, tzinfo=datetime.timezone.utc))]),
        ),
    ]
