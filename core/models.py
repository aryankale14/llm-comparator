from django.db import models
from django.contrib.auth.models import User

class UserQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    model_used = models.CharField(max_length=100, default="Multiple")


    gpt_response = models.TextField(blank=True, null=True)
    gemini_response = models.TextField(blank=True, null=True)
    mistral_response = models.TextField(blank=True, null=True)
    llama_response = models.TextField(blank=True, null=True)
    gemini_comparison = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

