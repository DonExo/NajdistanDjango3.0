# Generated by Django 3.0.4 on 2020-04-06 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_added_cover_image_to_the_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='slug',
            field=models.SlugField(default=1234, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
