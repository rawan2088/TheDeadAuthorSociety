# accounts/models.py
from django.db import models
from django.conf import settings

class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"