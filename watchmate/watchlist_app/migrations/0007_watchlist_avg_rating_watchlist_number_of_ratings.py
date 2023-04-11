# Generated by Django 4.1.7 on 2023-03-23 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0006_review_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='avg_rating',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='number_of_ratings',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
