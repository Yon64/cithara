from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .services.song_service import SongGenerationService
from .models.song import Song
import json

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
