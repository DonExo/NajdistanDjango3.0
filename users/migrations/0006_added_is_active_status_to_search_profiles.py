# Generated by Django 3.0.4 on 2020-04-11 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_added_unique_together_constraint'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchprofiles',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
