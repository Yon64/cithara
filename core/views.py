from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .services.song_service import SongGenerationService
import json

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
