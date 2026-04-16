from django.contrib import admin
from .models import Playlist, Song

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'display_playlists', 'status', 'audio_format', 'created_at')
    list_filter = ('status', 'mood', 'genre', 'audio_format')
    search_fields = ('title', 'user__username', 'prompt')
    readonly_fields = ('share_token', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'user', 'playlists', 'status')
        }),
        ('Generation Parameters', {
            'fields': ('prompt', 'reference_url', 'mood', 'occasion', 'genre', 'singer_gender', 'duration')
        }),
        ('Audio & Sharing', {
            'fields': ('audio_url', 'audio_format', 'share_token', 'created_at')
        }),
    )

    def display_playlists(self, obj):
        return ", ".join([p.name for p in obj.playlists.all()])
    display_playlists.short_description = 'Playlists'
