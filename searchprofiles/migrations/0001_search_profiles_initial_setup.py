# Generated by Django 3.0.4 on 2020-05-07 00:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0010_auto_20200428_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchProfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Name your Search Profile')),
                ('listing_type', models.CharField(choices=[('rent', 'For rent'), ('buy', 'For buy')], default='rent', help_text='Designates the type of search profile: rent or sell', max_length=10, verbose_name='Listing type')),
                ('rooms', models.PositiveSmallIntegerField(default=2, verbose_name='Number of rooms')),
                ('bedrooms', models.PositiveSmallIntegerField(default=1, verbose_name='Number of bedrooms')),
                ('min_price', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='Minimum price')),
                ('max_price', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='Maximum price')),
                ('interior', models.CharField(choices=[('unspecified', 'Not specified'), ('furnished', 'Fully furnished'), ('unfurnished', 'Non furnished'), ('upholstered', 'Semi furnished')], default='unspecified', max_length=15)),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('biweekly', 'Bi-weekly'), ('monthly', 'Monthly'), ('instant', 'Instantly')], default='weekly', max_length=255, verbose_name='Update frequency')),
                ('is_active', models.BooleanField(default=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='listings.Place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='searchprofiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Search profiles',
                'unique_together': {('user', 'title')},
            },
        ),
    ]
