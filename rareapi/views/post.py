"""View module for handling requests about posts"""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rareapi.models import Category
from rareapi.models import Post



class Posts(ViewSet):
    """Post"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized post instance
        """
        user = request.auth.user
        post = Post()

        try:
            post.title = request.data["title"]
            post.content = request.data["content"]
            post.publication_date = request.data["publication_date"]
            post.image_url = request.data["image_url"]
            post.approved = 1
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        post.user_id = user.id

        try:
            category = Category.objects.get(pk=request.data["category_id"])
            post.category_id = category.id
        except Category.DoesNotExist as ex:
            return Response({'message': 'Post type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        if user is not None:
            try:
                post.save()
                serializer = PostSerializer(post, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

class PostSerializer(serializers.ModelSerializer):
    """ JSON serializer for posts"""

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'approved')
        depth = 1