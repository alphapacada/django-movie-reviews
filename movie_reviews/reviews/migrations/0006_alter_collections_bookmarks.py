# Generated by Django 4.0.2 on 2022-02-27 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_movie_img_src'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collections',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='folders', to='reviews.Movie'),
        ),
    ]
