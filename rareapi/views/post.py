"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, RareUsers


class Posts(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

   

    def list(self, request):

        post = Post.objects.all()

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            posts = posts.filter(user_id=user_id)

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)




"""Serializer for RareUser Info in a post"""         
class PostRareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUsers
        fields = ('id', 'bio', 'fullname', 'username')

"""Basic Serializer for single post"""
class PostSerializer(serializers.ModelSerializer):
    user = PostRareUserSerializer(many=False)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'publication_date', 'content', 'user', 'category')
    