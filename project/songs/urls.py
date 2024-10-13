from django.urls import path
from .views import SongsListView, SongsSearchView, RatingView, UserRatedSongsView, QuerySongsView

urlpatterns = [
    path('', SongsListView.as_view(), name='songs-list'),
    path('search/', SongsSearchView.as_view(), name='songs-search'),
    path('query/', QuerySongsView.as_view(), name='query-song'),
]

urlpatterns += [
    path('rate-song/', RatingView.as_view(), name='rate-song'), 
    path('rated-songs/', UserRatedSongsView.as_view(), name='user-rated-songs'),
]