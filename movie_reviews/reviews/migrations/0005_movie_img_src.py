# Generated by Django 4.0.2 on 2022-02-27 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_collections_bookmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='img_src',
            field=models.URLField(default='https://static01.nyt.com/images/2021/11/23/arts/23encanto1/23encanto1-mediumThreeByTwo440.jpg'),
            preserve_default=False,
        ),
    ]