# Generated by Django 4.0.4 on 2022-08-10 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0003_silentlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='silentlist',
            name='confirmed_email',
            field=models.EmailField(default=1, max_length=256),
            preserve_default=False,
        ),
    ]
