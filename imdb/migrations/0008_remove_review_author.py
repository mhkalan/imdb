# Generated by Django 4.1.7 on 2023-04-02 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imdb', '0007_review_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
    ]
