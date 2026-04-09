from ..models.song import Song
from ..infrastructure.strategies import get_song_generator_strategy
from django.db import transaction

class SongGenerationService:
    """
    Application layer service for song generation.
    Uses the Strategy Pattern to support multiple generation backends.
    """
    
    def __init__(self, strategy=None):
        # The strategy can be injected, or fetched from the factory by default
        self.strategy = strategy or get_song_generator_strategy()

    def generate_song(self, user, title, prompt, genre, mood, occasion, singer_gender, audio_format='MP3'):
        """
        Main use case: Generate a song for a user using the active strategy.
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
            # 2. Call the active strategy
            result = self.strategy.generate(
                prompt=prompt,
                genre=genre,
                mood=mood,
                title=title
            )
            
            # 3. Update Song with results
            # The strategy returns a dictionary with 'suno_id' and initial 'status'
            song.suno_id = result.get('suno_id')
            
            # If the strategy returns an audio_url immediately (like Mock), use it
            if result.get('audio_url'):
                song.audio_url = result.get('audio_url')
            
            # Update status based on strategy result
            song.status = result.get('status', 'Generating')
            song.save()
            return song
        except Exception as e:
            song.status = 'Failed'
            song.save()
            raise e

    def update_song_status(self, song_id):
        """
        Polls the strategy for the latest status and updates the song in DB.
        """
        song = Song.objects.get(id=song_id)
        
        # If already Ready or Failed, no need to poll
        if song.status in ['Ready', 'Failed']:
            return song

        # If we don't have a suno_id, we can't poll
        if not song.suno_id:
            return song

        try:
            # Call the strategy to get the latest status
            result = self.strategy.get_status(song.suno_id)
            
            # Update song fields
            song.status = result.get('status', song.status)
            if result.get('audio_url'):
                song.audio_url = result.get('audio_url')
            
            song.save()
            
            # Add raw status for UI feedback
            song.raw_status = result.get('raw_status')
            return song
        except Exception as e:
            print(f"Error updating song status: {e}")
            return song
