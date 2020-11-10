"""Post model module"""
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """Post database model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    publication_date = models.IntegerField()
    image_url = models.CharField(max_length=256)
