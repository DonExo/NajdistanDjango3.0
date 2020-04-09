from rest_framework import serializers

from listings.models import Listing, Comment, HeatingChoices, Place
from reports.models import ListingReport, CommentReport
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'email', 'telephone', )

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request', None)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class ListingReportSerializer(serializers.HyperlinkedModelSerializer):
    reporter = serializers.CharField(read_only=True)
    listing = serializers.CharField(read_only=True)

    class Meta:
        model = ListingReport
        fields = ('reporter', 'listing', 'reason', )


class CommentReportSerializer(serializers.HyperlinkedModelSerializer):
    reporter = serializers.CharField(read_only=True)
    comment = serializers.CharField(read_only=True)

    class Meta:
        model = CommentReport
        fields = ('reporter', 'comment', 'reason', )


class HeatingChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatingChoices
        fields = ('name', )


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = ('region', 'city', )


class ListingSerializer(serializers.HyperlinkedModelSerializer):
    heating = HeatingChoicesSerializer(read_only=True, many=True)

    class Meta:
        model = Listing
        fields = ('url', 'user', 'city', 'title', 'description', 'address', 'zip_code', 'home_type', 'quadrature', 'rooms', 'bedrooms',
                  'floor', 'interior', 'heating', 'price', 'basement', 'parking', 'elevator', 'balcony',
                  'is_available', 'available_from', 'rental_period', 'listing_type', )
