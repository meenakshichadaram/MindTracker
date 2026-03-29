from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        (1, 'Terrible'),
        (2, 'Very Bad'),
        (3, 'Bad'),
        (4, 'Low'),
        (5, 'Neutral'),
        (6, 'Okay'),
        (7, 'Good'),
        (8, 'Great'),
        (9, 'Excellent'),
        (10, 'Amazing'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    score = models.IntegerField(choices=MOOD_CHOICES)
    note = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    sleep_hours = models.FloatField(null=True, blank=True)
    energy_level = models.IntegerField(null=True, blank=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.score}/10'