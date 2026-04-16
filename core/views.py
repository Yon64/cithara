from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .services.song_service import SongGenerationService
from .models.song import Song
from .models.playlist import Playlist
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class SongCreatePageView(TemplateView):
    template_name = 'core/song_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass choices to the template for the form selects
        context['moods'] = Song.MOOD_CHOICES
        context['occasions'] = Song.OCCASION_CHOICES
        context['genres'] = Song.GENRE_CHOICES
        context['genders'] = Song.GENDER_CHOICES
        return context

@method_decorator(csrf_exempt, name='dispatch')
class SongCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            # For simplicity, we'll use a hardcoded user or the first one if it exists
            from django.contrib.auth.models import User
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(username='admin', password='password')

            service = SongGenerationService()
            song = service.generate_song(
                user=user,
                title=data.get('title', 'Untitled AI Song'),
                prompt=data.get('prompt', 'A beautiful melody'),
                genre=data.get('genre', 'Pop'),
                mood=data.get('mood', 'Happy'),
                occasion=data.get('occasion', 'Party'),
                singer_gender=data.get('singer_gender', 'Female')
            )
            
            return JsonResponse({
                'id': song.id,
                'title': song.title,
                'status': song.status,
                'audio_url': song.audio_url,
                'share_token': str(song.share_token)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class SongStatusView(View):
    def get(self, request, song_id, *args, **kwargs):
        try:
            service = SongGenerationService()
            song = service.update_song_status(song_id)
            
            return JsonResponse({
                'id': song.id,
                'title': song.title,
                'status': song.status,
                'raw_status': getattr(song, 'raw_status', None),
                'audio_url': song.audio_url,
                'share_token': str(song.share_token)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class LibraryPageView(TemplateView):
    template_name = 'core/library.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.first()
        if user:
            context['songs'] = Song.objects.filter(user=user).prefetch_related('playlists').order_by('-created_at')
            context['playlists'] = Playlist.objects.filter(user=user).order_by('-created_at')
        else:
            context['songs'] = []
            context['playlists'] = []
        # Pass model choices for dynamic filter dropdowns 
        context['moods'] = Song.MOOD_CHOICES
        context['genres'] = Song.GENRE_CHOICES
        context['occasions'] = Song.OCCASION_CHOICES
        context['statuses'] = Song.STATUS_CHOICES
        context['genders'] = Song.GENDER_CHOICES
        return context

@method_decorator(csrf_exempt, name='dispatch')
class SongRenameView(View):
    def post(self, request, song_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            # Use a hardcoded user or the first one if it exists
            user = User.objects.first()
            if not user:
                return JsonResponse({'error': 'Not authenticated'}, status=401)
            
            song = get_object_or_404(Song, id=song_id, user=user)
            new_title = data.get('title')
            if not new_title:
                return JsonResponse({'error': 'Title is required'}, status=400)
            
            song.title = new_title
            song.save()
            return JsonResponse({'status': 'success', 'title': song.title})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class SongDeleteView(View):
    def delete(self, request, song_id, *args, **kwargs):
        try:
            user = User.objects.first()
            if not user:
                return JsonResponse({'error': 'Not authenticated'}, status=401)
            
            song = get_object_or_404(Song, id=song_id, user=user)
            song.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class PlaylistCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = User.objects.first()
            if not user:
                return JsonResponse({'error': 'Not authenticated'}, status=401)
            
            name = data.get('name')
            if not name:
                return JsonResponse({'error': 'Playlist name is required'}, status=400)
            
            playlist = Playlist.objects.create(name=name, user=user)
            return JsonResponse({'status': 'success', 'id': playlist.id, 'name': playlist.name})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class SongUpdatePlaylistView(View):
    def post(self, request, song_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = User.objects.first()
            if not user:
                return JsonResponse({'error': 'Not authenticated'}, status=401)
            
            song = get_object_or_404(Song, id=song_id, user=user)
            playlist_id = data.get('playlist_id')
            action = data.get('action')
            
            if playlist_id and action in ['add', 'remove']:
                playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
                if action == 'add':
                    song.playlists.add(playlist)
                elif action == 'remove':
                    song.playlists.remove(playlist)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'error': 'Invalid parameters'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
