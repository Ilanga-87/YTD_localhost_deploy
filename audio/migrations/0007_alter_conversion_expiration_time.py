# Generated by Django 4.0.6 on 2023-02-26 14:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0006_silentlist_input_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversion',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 27, 14, 20, 53, 867516, tzinfo=utc), verbose_name='Burn time'),
        ),
    ]
