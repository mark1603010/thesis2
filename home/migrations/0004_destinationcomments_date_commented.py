# Generated by Django 3.1.7 on 2022-03-10 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20220310_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='destinationcomments',
            name='date_commented',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
