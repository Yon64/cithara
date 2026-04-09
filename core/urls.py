from django.urls import path
from .views import SongCreateView, SongCreatePageView, SongStatusView

urlpatterns = [
    path('generate-song/', SongCreateView.as_view(), name='generate-song'),
    path('song-status/<int:song_id>/', SongStatusView.as_view(), name='song-status'),
    path('', SongCreatePageView.as_view(), name='song-create-page'),
]
