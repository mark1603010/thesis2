# Generated by Django 3.1.7 on 2022-07-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20220705_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportcomment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
