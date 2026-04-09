from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import MagicMock
from ..services.song_service import SongGenerationService
from ..models.song import Song

class SongGenerationServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.mock_strategy = MagicMock()
        self.service = SongGenerationService(strategy=self.mock_strategy)

    def test_generate_song_success(self):
        # Setup mock return value
        self.mock_strategy.generate.return_value = {
            "suno_id": "test-suno-123",
            "audio_url": "http://example.com/audio.mp3",
            "status": "Ready"
        }

        # Call service
        song = self.service.generate_song(
            user=self.user,
            title="Test Song",
            prompt="A test prompt",
            genre="Pop",
            mood="Happy",
            occasion="Party",
            singer_gender="Female"
        )

        # Assertions
        self.assertEqual(song.title, "Test Song")
        self.assertEqual(song.status, "Ready")
        self.assertEqual(song.suno_id, "test-suno-123")
        self.assertEqual(song.audio_url, "http://example.com/audio.mp3")
        self.mock_strategy.generate.assert_called_once()

    def test_generate_song_failure(self):
        # Setup mock to raise exception
        self.mock_strategy.generate.side_effect = Exception("API Error")

        # Call service and assert exception
        with self.assertRaises(Exception):
            self.service.generate_song(
                user=self.user,
                title="Fail Song",
                prompt="A test prompt",
                genre="Pop",
                mood="Happy",
                occasion="Party",
                singer_gender="Female"
            )

        # Check song status in DB
        song = Song.objects.get(title="Fail Song")
        self.assertEqual(song.status, "Failed")
