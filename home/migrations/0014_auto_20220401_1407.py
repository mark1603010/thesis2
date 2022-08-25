# Generated by Django 3.1.7 on 2022-04-01 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20220313_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinationlike',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_likes', to='home.destination'),
        ),
        migrations.AlterField(
            model_name='destinationlike',
            name='like',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_destination_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_ratings', to='home.destination')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_rating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='destination',
            name='ratings',
            field=models.ManyToManyField(related_name='user_ratings', through='home.UserRating', to=settings.AUTH_USER_MODEL),
        ),
    ]