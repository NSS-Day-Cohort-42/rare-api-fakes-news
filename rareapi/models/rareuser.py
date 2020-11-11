"""Database RareUser module"""
from django.db import models
from django.contrib.auth.models import User


class RareUser(models.Model):
    """RareUser database model"""
    bio = models.CharField(max_length=500)
    profile_image_url = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

