from django.db import models
from user_manager.models import User


class Intent(models.Model):
    username = models.ForeignKey(User, related_name="intents", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    intent_string = models.TextField()
