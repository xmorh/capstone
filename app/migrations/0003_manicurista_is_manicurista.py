# Generated by Django 3.1 on 2024-11-06 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20241105_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='manicurista',
            name='is_manicurista',
            field=models.BooleanField(default=False),
        ),
    ]
