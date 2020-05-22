# Generated by Django 3.0.4 on 2020-05-22 21:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_rename_plural_version_of_Bookmarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[0-9]*$', message="Phone number should be a combination of numbers and '+' sign (i.e. +31612341234 or 0612341234)")], verbose_name='Phone number'),
        ),
    ]
