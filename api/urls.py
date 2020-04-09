from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, ListingReportViewSet, CommentReportViewSet, ListingViewSet, PlaceViewSet

api_router = DefaultRouter()
api_router.register('users', UserViewSet, 'user')
api_router.register('listingreports', ListingReportViewSet, 'listingreport')
api_router.register('commentreports', CommentReportViewSet, 'commentreport')
api_router.register('listings', ListingViewSet, 'listing')
api_router.register('places', PlaceViewSet, 'place')


urlpatterns = [
    path('', include(api_router.urls)),
    path('admin/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
