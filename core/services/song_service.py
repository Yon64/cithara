from ..models.song import Song
from ..infrastructure.suno_client import SunoClient
from django.db import transaction

class SongGenerationService:
    """
    Application layer service for song generation.
    Orchestrates the domain model and infrastructure client.
    """
    
    def __init__(self, suno_client=None):
        self.suno_client = suno_client or SunoClient()

    def generate_song(self, user, title, prompt, genre, mood, occasion, singer_gender, audio_format='MP3'):
        """
        Main use case: Generate a song for a user.
        """
        # 1. Create Song in 'Generating' status
        song = Song.objects.create(
            user=user,
            title=title,
            prompt=prompt,
            genre=genre,
            mood=mood,
            occasion=occasion,
            singer_gender=singer_gender,
            status='Generating',
            audio_format=audio_format
        )
        
        try:
            # 2. Call SUNO API via Infrastructure client
            result = self.suno_client.generate(
                prompt=prompt,
                genre=genre,
                mood=mood
            )
            
            # 3. Update Song with results
            song.suno_id = result.get('suno_id')
            song.audio_url = result.get('audio_url')
            song.status = 'Ready'
            song.save()
            
            return song
            
        except Exception as e:
            # Handle failure
            song.status = 'Failed'
            song.save()
            raise e
