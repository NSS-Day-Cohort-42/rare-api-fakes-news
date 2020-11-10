"""Post model module"""
from django.db import models
# from . import RareUser, Category




class Post(models.Model):
    """Post database model"""

    user = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rareuser")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category")
    title = models.CharField(max_length=75)
    publication_date = models.IntegerField()
    image_url = models.CharField(max_length=256)
    content = models.TextField()
    approved = models.BooleanField(default=False)
