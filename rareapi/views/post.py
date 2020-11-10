from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class Posts(ViewSet):
    """Rare posts"""

    def create(self, request):
        """Handle POST operations for posts

        Returns:
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.publication_date = request.data["date"]
        post.image_url = request.data["image_url"]
        post.approved = request.data["approved"]

        category = Post.objects.get(pk=request.data["category_id"])
        post.category = category

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)