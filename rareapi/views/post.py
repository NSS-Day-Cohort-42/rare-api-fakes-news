"""View module for handling requests about posts"""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post



class Posts(ViewSet):
    """Post"""

    def list(self, request):
        """Handle GET requests to post resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all post records from the database
        posts = Post.objects.all()

        user = request.auth.user

        if user is not None:
            posts = posts.filter(user_id = user.id)

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class PostSerializer(serializers.ModelSerializer):
    """ JSON serializer for posts"""

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url')