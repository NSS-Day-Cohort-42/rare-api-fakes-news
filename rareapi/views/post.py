"""View module for handling requests about games"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rareapi.models import Category
from rareapi.models import Post
from rareapi.models import RareUser


class Posts(ViewSet):

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

        posts = Post.objects.all()

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            posts = posts.filter(user_id=user_id)

        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

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
    
    def update(self, request, pk=None):
        """Handle PUT requests for posts"""

        rareuser = RareUser.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.rareuser = rareuser

        category = Category.objects.get(pk=request.data["category"])
        post.category = category
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        
      
   
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',)



"""Serializer for RareUser Info in a post"""         
class PostRareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'user')
        

"""Basic Serializer for single post"""
class PostSerializer(serializers.ModelSerializer):
    user = PostRareUserSerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'content', 'user', 'category', 'approved', 'image_url')
        depth = 1
    
