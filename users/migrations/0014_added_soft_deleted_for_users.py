# Generated by Django 3.0.4 on 2020-05-28 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_change_phone_regex_validation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='soft_delete',
            field=models.BooleanField(default=False, null=True),
        ),
    ]