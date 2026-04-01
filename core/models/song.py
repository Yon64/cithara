import uuid
from django.db import models
from django.contrib.auth.models import User
from .playlist import Playlist

class Song(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Generating', 'Generating'),
        ('Ready', 'Ready'),
        ('Failed', 'Failed'),
    ]

    MOOD_CHOICES = [
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Energetic', 'Energetic'),
        ('Calm', 'Calm'),
        ('Angry', 'Angry'),
    ]

    OCCASION_CHOICES = [
        ('Wedding', 'Wedding'),
        ('Party', 'Party'),
        ('Workout', 'Workout'),
        ('Study', 'Study'),
        ('Relaxation', 'Relaxation'),
    ]

    GENRE_CHOICES = [
        ('Pop', 'Pop'),
        ('Rock', 'Rock'),
        ('Jazz', 'Jazz'),
        ('Classical', 'Classical'),
        ('Electronic', 'Electronic'),
        ('Hip-Hop', 'Hip-Hop'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-binary', 'Non-binary'),
    ]

    FORMAT_CHOICES = [
        ('MP3', 'MP3'),
        ('M4A', 'M4A'),
    ]

    title = models.CharField(max_length=255)
    prompt = models.TextField()
    reference_url = models.URLField(blank=True, null=True, help_text="Optional reference song URL")
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES)
    occasion = models.CharField(max_length=50, choices=OCCASION_CHOICES)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    singer_gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    audio_url = models.URLField(blank=True, null=True)
    audio_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='MP3')
    duration = models.DurationField(blank=True, null=True)
    share_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    suno_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs', blank=True, null=True)

    def __str__(self):
        return self.title
