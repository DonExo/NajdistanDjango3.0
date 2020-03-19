# Generated by Django 3.0.4 on 2020-03-19 00:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HeatingChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Heating type')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('address', models.CharField(blank=True, max_length=80, verbose_name='Address')),
                ('zip_code', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(code='invalid_zipcode', message='Zip code must be in format 1234AB', regex='^[0-9]{4}[a-zA-Z]{2}$')], verbose_name='Zip-code')),
                ('home_type', models.CharField(choices=[('house', 'A house'), ('apartment', 'An apartment')], default='house', help_text='Designates the type of home: House or Apartment', max_length=10, verbose_name='Type of home')),
                ('quadrature', models.PositiveSmallIntegerField(verbose_name='Quadrature')),
                ('rooms', models.PositiveSmallIntegerField(verbose_name='Rooms')),
                ('bedrooms', models.PositiveSmallIntegerField(verbose_name='Bedrooms')),
                ('floor', models.PositiveSmallIntegerField(verbose_name='Floor')),
                ('interior', models.CharField(choices=[('unspecified', 'Not specified'), ('furnished', 'Fully furnished'), ('unfurnished', 'Non furnished'), ('upholstered', 'Semi furnished')], default='unspecified', max_length=255)),
                ('price', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='Price in EUR')),
                ('basement', models.BooleanField(default=False, verbose_name='Basement')),
                ('parking', models.BooleanField(default=False, verbose_name='Parking place')),
                ('elevator', models.BooleanField(default=False, verbose_name='Elevator')),
                ('balcony', models.BooleanField(default=False, verbose_name='Balcony')),
                ('times_visited', models.PositiveIntegerField(default=0, verbose_name='Times visited')),
                ('is_available', models.BooleanField(default=True, verbose_name='Available?')),
                ('available_from', models.DateField(blank=True, null=True)),
                ('rental_period', models.PositiveSmallIntegerField(blank=True, default=6, null=True, verbose_name='Minimum rental period (in months)')),
                ('is_approved', models.NullBooleanField(default=None, verbose_name='Approved?')),
                ('rejection_reason', models.CharField(blank=True, max_length=255, null=True, verbose_name='Rejection reason')),
                ('listing_type', models.CharField(choices=[('rent', 'For rent'), ('sell', 'For sell')], default='rent', help_text='Designates the type of listings: rent or sell', max_length=10, verbose_name='Listing type')),
                ('soft_deleted', models.BooleanField(default=False, verbose_name='Soft deleted')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255, verbose_name='Region')),
                ('city', models.CharField(max_length=255, verbose_name='City')),
            ],
            options={
                'unique_together': {('region', 'city')},
            },
        ),
        migrations.CreateModel(
            name='SearchProfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Search profile title')),
                ('rooms', models.PositiveSmallIntegerField(default=1, verbose_name='Minimum number of rooms')),
                ('bedrooms', models.PositiveSmallIntegerField(default=1, verbose_name='Minimum number of bedrooms')),
                ('price_from', models.PositiveIntegerField(default=1, verbose_name='Price from')),
                ('price_to', models.PositiveIntegerField(default=1000, verbose_name='Price to')),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('biweekly', 'Bi-weekly'), ('monthly', 'Monthly'), ('instant', 'Instantly')], default='weekly', max_length=255, verbose_name='Update frequency')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='searchprofiles', to='listings.Place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='searchprofiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Saved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to='listings.Listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings', to='listings.Place'),
        ),
        migrations.AddField(
            model_name='listing',
            name='heating',
            field=models.ManyToManyField(to='listings.HeatingChoices'),
        ),
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('body', models.TextField(verbose_name='Comment body')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='listings.Listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
