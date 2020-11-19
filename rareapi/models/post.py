"""Post model module"""
from django.db import models

class Post(models.Model):
    """Post database model"""

    user = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rareuser")
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null = True, related_name="category")
    title = models.CharField(max_length=75)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=256)
    content = models.TextField()
    approved = models.BooleanField(default=False)


    @property
    def created_by_current_user(self):
        return self.__created_by_current_user

    @created_by_current_user.setter
    def created_by_current_user(self, value):
        self.__created_by_current_user = value

