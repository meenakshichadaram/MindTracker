from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WeeklyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_reports')
    week_start = models.DateField()
    week_end = models.DateField()
    avg_mood = models.FloatField()
    total_entries = models.IntegerField()
    best_day = models.DateField(null=True, blank=True)
    worst_day = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - week of {self.week_start}'