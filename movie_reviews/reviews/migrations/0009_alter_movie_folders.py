# Generated by Django 4.0.2 on 2022-02-28 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_alter_collections_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='folders',
            field=models.ManyToManyField(to='reviews.Collections'),
        ),
    ]
