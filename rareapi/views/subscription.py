from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Subscription
from django.contrib.auth.models import User
from rareapi.models import RareUser


class Subscriptions(ViewSet):

    def list(self, request):

        # following = RareUser.objects.get(user=request.auth.user)

        followings = Subscription.objects.all()
        serializer = SubscriptionSerializer(followings, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            following = Following.objects.get(pk=pk)
            serializer = FollowingSerializer(
                following, context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_following = Following()

        new_following.user = request.auth.user
        new_following.following = User.objects.get(pk=request.data["following_id"])

        new_following.save()

        serializer = FollowingSerializer(
            new_following, context={'request': request}
        )
        return Response(serializer.data)

    def patch(self, request, pk=None):
        try:
            post = SneakerPost.objects.get(pk=pk)
            post.description = request.data["description"]

            serializer = PostSerializer(post, context={'request': request}, partial=True)

            post.save()

            return Response(status=status.HTTP_201_CREATED, data=serializer.data)

        except SneakerPost.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('first_name',)

# class RareUserSerializer(serializers.ModelSerializer):
#     """Serializer for RareUser Info from a post"""
#     user = UserSerializer(many=False)

#     class Meta:
#         model = RareUser
#         fields = ('id', 'bio', 'user')

class SubscriptionSerializer(serializers.ModelSerializer):
    # author = UserSerializer(many=False)

    class Meta:
        model = Subscription
        fields = ('id', 'created_on', 'ended_on', 'author', 'follower')
        # depth = 1