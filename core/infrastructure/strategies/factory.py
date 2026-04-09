from django.conf import settings
from .mock import MockSongGeneratorStrategy
from .suno import SunoSongGeneratorStrategy

def get_song_generator_strategy():
    """
    Factory function to select and return the active song generation strategy.
    Selection is based on the GENERATOR_STRATEGY setting in settings.py.
    """
    strategy_type = getattr(settings, 'GENERATOR_STRATEGY', 'mock').lower()

    if strategy_type == 'suno':
        return SunoSongGeneratorStrategy()
    else:
        # Default to mock strategy
        return MockSongGeneratorStrategy()
