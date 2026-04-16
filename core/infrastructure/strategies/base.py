from abc import ABC, abstractmethod

class SongGeneratorStrategy(ABC):
    """
    Abstract interface for song generation strategies.
    Any new generation implementation must inherit from this class.
    """

    @abstractmethod
    def generate(self, prompt, genre=None, mood=None, instrumental=False, title=None):
        """
        Triggers song generation.
        Returns a dictionary with generation result (e.g., suno_id, audio_url).
        """
        pass

    @abstractmethod
    def get_status(self, task_id):
        """
        Checks the status of a generation task.
        """
        pass
