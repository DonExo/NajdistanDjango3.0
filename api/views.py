from rest_framework import viewsets, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.serializers import UserSerializer, ListingReportSerializer, CommentReportSerializer, ListingSerializer, PlaceSerializer
from users.models import User
from listings.models import Listing, Comment, Place
from reports.models import ListingReport, CommentReport


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    lookup_field = 'pk'
    queryset = User.objects.all()


class ListingReportViewSet(viewsets.ModelViewSet):
    serializer_class = ListingReportSerializer
    lookup_field = 'pk'
    queryset = ListingReport.objects.all()


class CommentReportViewSet(viewsets.ModelViewSet):
    serializer_class = CommentReportSerializer
    lookup_field = 'pk'
    queryset = CommentReport.objects.all()


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    lookup_field = 'pk'
    permission_classes = []
    queryset = Listing.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)

        if partial is False:
            raise exceptions.MethodNotAllowed(request.Method)
        return super(self, ListingViewSet).update(self, *args, **kwargs)


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    lookup_field = 'pk'
    queryset = Place.objects.all()