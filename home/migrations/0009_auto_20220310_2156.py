# Generated by Django 3.1.7 on 2022-03-10 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_destination_date_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destination',
            old_name='date_created',
            new_name='date_posted',
        ),
    ]
