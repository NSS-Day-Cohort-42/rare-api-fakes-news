from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rareapi.models import Post, Category, RareUser


class Posts(ViewSet):
    """Rare posts"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(user=request.auth.user)
        post = Post()

        try:
            post.title = request.data["title"]
            post.content = request.data["content"]
            post.publication_date = request.data["date"]
            post.image_url = ""
            post.approved = 1
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        post.user = user

        try:
            category = Post.objects.get(pk=request.data["category_id"])
            post.category = category
        except Category.DoesNotExist as ex:
            return Response({'message': 'Post type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

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