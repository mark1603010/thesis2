# Generated by Django 3.1.7 on 2022-03-10 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_destination_posted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
