from django.test import TestCase, override_settings
from ..infrastructure.strategies import get_song_generator_strategy, MockSongGeneratorStrategy, SunoSongGeneratorStrategy

class StrategyFactoryTest(TestCase):
    @override_settings(GENERATOR_STRATEGY='mock')
    def test_factory_returns_mock_strategy(self):
        strategy = get_song_generator_strategy()
        self.assertIsInstance(strategy, MockSongGeneratorStrategy)

    @override_settings(GENERATOR_STRATEGY='suno')
    def test_factory_returns_suno_strategy(self):
        strategy = get_song_generator_strategy()
        self.assertIsInstance(strategy, SunoSongGeneratorStrategy)

    @override_settings(GENERATOR_STRATEGY='invalid')
    def test_factory_defaults_to_mock_on_invalid_setting(self):
        strategy = get_song_generator_strategy()
        self.assertIsInstance(strategy, MockSongGeneratorStrategy)

class MockStrategyTest(TestCase):
    def setUp(self):
        self.strategy = MockSongGeneratorStrategy()

    def test_generate_returns_mock_data(self):
        result = self.strategy.generate(prompt="Test prompt")
        self.assertTrue(result['suno_id'].startswith("mock-"))
        self.assertEqual(result['status'], "Ready")
        self.assertEqual(result['audio_url'], "https://cdn1.suno.ai/sample1.mp3")

    def test_get_status_returns_ready(self):
        result = self.strategy.get_status("some-id")
        self.assertEqual(result['status'], "Ready")

class SunoStrategyTest(TestCase):
    @override_settings(SUNO_API_TOKEN='test-token')
    def setUp(self):
        self.strategy = SunoSongGeneratorStrategy()

    def test_initialization_with_settings(self):
        self.assertEqual(self.strategy.api_token, 'test-token')
        self.assertEqual(self.strategy.base_url, "https://api.sunoapi.org/api/v1")
