"""Post model module"""
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """Post database model"""
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=256)
    content = models.CharField(max_length=1000)
    approved = models.BooleanField(default=False)