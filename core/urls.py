from django.urls import path
from .views import SongCreateView, SongCreatePageView, SongStatusView, LibraryPageView, SongRenameView, SongDeleteView, PlaylistCreateView, SongUpdatePlaylistView

urlpatterns = [
    path('generate-song/', SongCreateView.as_view(), name='generate-song'),
    path('song-status/<int:song_id>/', SongStatusView.as_view(), name='song-status'),
    path('library/', LibraryPageView.as_view(), name='library'),
    path('api/songs/<int:song_id>/rename/', SongRenameView.as_view(), name='song-rename'),
    path('api/songs/<int:song_id>/delete/', SongDeleteView.as_view(), name='song-delete'),
    path('api/songs/<int:song_id>/playlist/', SongUpdatePlaylistView.as_view(), name='song-update-playlist'),
    path('api/playlists/create/', PlaylistCreateView.as_view(), name='playlist-create'),
    path('', SongCreatePageView.as_view(), name='song-create-page'),
]
