# Generated by Django 3.1.7 on 2022-07-09 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20220709_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='destination',
            name='long',
        ),
        migrations.RemoveField(
            model_name='destination',
            name='manual_address',
        ),
    ]
