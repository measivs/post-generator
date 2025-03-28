from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Session(models.Model):
    """
    A session represents a single conversation between a user and the chatbot.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Session {self.id} - {self.user}"


class Chat(models.Model):
    """
    A Chat model stores each message sent in a conversation session.
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="chats")
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    message = models.TextField()
    generated_content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.capitalize()} - {self.message[:30]}"
