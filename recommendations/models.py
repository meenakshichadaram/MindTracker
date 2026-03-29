from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Recommendation(models.Model):
    CATEGORY_CHOICES = [
        ('mindfulness', 'Mindfulness'),
        ('exercise', 'Exercise'),
        ('sleep', 'Sleep'),
        ('social', 'Social'),
        ('diet', 'Diet'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_read = models.BooleanField(default=False)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.title}'