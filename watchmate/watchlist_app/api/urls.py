from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api import views
from watchlist_app.api.views import StreamPlatformVS


router = DefaultRouter()
router.register('stream-platforms', StreamPlatformVS, basename='stream-platforms')


urlpatterns = [
    path('', include(router.urls)), 
    path('shows/', views.AllWatchListAV.as_view(), name='all-watchlist-detail'),
    path('shows/<int:id>/', views.AllWatchListDetailAV.as_view(), name='watchlist-detail'),
    path('stream-platforms/<int:pk>/shows/', views.StreamPlatformWatchListAV.as_view(), name='stream-watchlist-list'), 
    path('shows/search/', views.SearchShows.as_view(), name='search-watchlist-list'), 
    path('shows/ordering/', views.OrderingShows.as_view(), name='ordering-watchlist-list'), 
    path('reviews/', views.AllReviewAV.as_view(), name='all-reviews'),
    path('reviews/<int:pk>/', views.ReviewDetailAV.as_view(), name='reviews-detail'),
    path('reviews/my-reviews/', views.UserReviewAV.as_view(), name='my-reviews'),
    path('reviews/<str:username>/', views.UserReviewListAV.as_view(), name='user-reviews'),
    path('reviews-params/', views.UserParamReviewListAV.as_view(), name='user-params'),
    path('reviews-filter/', views.AllReviewListFilterAV.as_view(), name='review-filter'),
    path('shows/<int:pk>/create-review/', views.ReviewCreateAV.as_view(), name='reviews-create'),
    path('shows/<int:pk>/reviews/', views.ReviewListAV.as_view(), name='reviews-list'),
]
 