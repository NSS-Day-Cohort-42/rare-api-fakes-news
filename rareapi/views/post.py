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
from rareapi.models import Tag


class Posts(ViewSet):

    def list(self, request):

        posts = Post.objects.all()
        approvedPosts = []

        for post in posts:
            if post.approved == True:
                approvedPosts.append(post)

        for post in posts:
            post.created_by_current_user = None

            if post.user.id == request.auth.user.id:
                post.created_by_current_user = True
            else:
                post.created_by_current_user = False

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            posts = posts.filter(user_id=user_id)

        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            posts = posts.filter(category_id=category_id)

        serializer = PostSerializer(
            approvedPosts, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            post = Post.objects.get(pk=pk)
            if post.user.id == request.auth.user.id:
                post.created_by_current_user = True
            else:
                post.created_by_current_user = False
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

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
            post.approved = 0
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


    def update(self, request, pk=None):
        """Handle PUT requests for posts"""
       
        rareuser = RareUser.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.user = rareuser

        category = Category.objects.get(pk=request.data["category_id"])
        post.category = category
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        

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





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',)

class PostRareUserSerializer(serializers.ModelSerializer):
    """Serializer for RareUser Info from a post"""
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'user')



# class PostTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('id', 'label')

class PostSerializer(serializers.ModelSerializer):
    """Basic Serializer for a post"""
    user = PostRareUserSerializer(many=False)
    # tags = PostTagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'content',
                  'user', 'category_id', 'category', 'approved', 'image_url', 'created_by_current_user')
        depth = 1
