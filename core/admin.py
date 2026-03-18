from django.contrib import admin
from .models import Playlist, Song

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'playlist', 'status', 'created_at')
    list_filter = ('status', 'mood', 'genre')
    search_fields = ('title', 'user__username', 'prompt')
