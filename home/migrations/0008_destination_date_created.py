# Generated by Django 3.1.7 on 2022-03-10 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20220310_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
