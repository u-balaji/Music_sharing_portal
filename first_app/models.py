from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Song(models.Model):
    SONG_CHOICES = [
        ("Public", "Public"),
        ("Private", "Private"),
        ('Protected', 'Protected')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_name = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='', blank=True, null=True)
    audio_type = models.CharField(max_length=20, choices=SONG_CHOICES,default="Public")
    allowed_emails = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username + "  " + self.audio_name



