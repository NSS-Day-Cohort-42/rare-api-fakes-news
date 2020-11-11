"""Reaction model module"""
from django.db import models


class Reaction(models.Model):
    """Reaction database model"""
    label = models.CharField(max_length=25)
    image_url = models.CharField(max_length=256)