# Generated by Django 4.1.7 on 2023-04-02 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imdb', '0009_review_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='averageRating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='content',
            name='totalNumberOfRatings',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
