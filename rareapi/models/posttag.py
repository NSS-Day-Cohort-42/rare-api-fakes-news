"""PostTag model module"""
from django.db import models
# from . import Post, Tag


class PostTag(models.Model):
    """PostTag database model"""
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="tag" )
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="posttag" )
