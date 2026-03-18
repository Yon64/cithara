from django.db import models
from django.contrib.auth.models import User

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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

    title = models.CharField(max_length=255)
    prompt = models.TextField()
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES)
    occasion = models.CharField(max_length=50, choices=OCCASION_CHOICES)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    singer_gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    audio_url = models.URLField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')

    def __str__(self):
        return self.title
