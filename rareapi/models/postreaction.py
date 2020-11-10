"""PostReaction model module"""
from django.db import models
# from . import RareUser, Post, Reaction 


class PostReaction(models.Model):
    """PostReaction database model"""
    user= models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rareuserreaction" )
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="reaction" )
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="postreaction" )
