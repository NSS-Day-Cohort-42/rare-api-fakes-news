from django.http import HttpResponseServerError
from rest_framework.fields import NullBooleanField
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Subscription
from django.contrib.auth.models import User
from rareapi.models import RareUser
from datetime import date


class Subscriptions(ViewSet):

    def list(self, request):

        # following = RareUser.objects.get(user=request.auth.user)

        followings = Subscription.objects.all()
        serializer = SubscriptionSerializer(followings, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        new_subscription = Subscription()

        new_subscription.follower = request.auth.user
        new_subscription.author = User.objects.get(pk=request.data["author_id"])
        new_subscription.created_on = date.today()

        new_subscription.save()

        serializer = SubscriptionSerializer(new_subscription, context={'request': request})
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



class SubscriptionSerializer(serializers.ModelSerializer):
    # author = UserSerializer(many=False)

    class Meta:
        model = Subscription
        fields = ('id', 'created_on', 'ended_on', 'author', 'follower')
        # depth = 1