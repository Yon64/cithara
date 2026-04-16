import uuid
from .base import SongGeneratorStrategy

class MockSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Mock strategy for offline development and deterministic testing.
    """

    def generate(self, prompt, genre=None, mood=None, instrumental=False, title=None):
        """
        Returns a mock response immediately.
        """
        suno_id = f"mock-{uuid.uuid4()}"
        return {
            "suno_id": suno_id,
            "audio_url": "https://cdn1.suno.ai/sample1.mp3",
            "status": "Ready",
            "metadata": {
                "prompt": prompt,
                "genre": genre,
                "mood": mood,
                "mock": True
            }
        }

    def get_status(self, task_id):
        """
        Always returns Ready for mock tasks.
        """
        return {
            "suno_id": task_id,
            "status": "Ready",
            "audio_url": "https://cdn1.suno.ai/sample1.mp3"
        }
