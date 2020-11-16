from rareapi.models import subscription
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

        user = RareUser.objects.get(user=request.auth.user)
        new_subscription.follower = user

        new_subscription.author = RareUser.objects.get(pk=request.data["author_id"])
        new_subscription.created_on = date.today()

        new_subscription.save()

        serializer = SubscriptionSerializer(new_subscription, context={'request': request})
        return Response(serializer.data)

    # @action(methods=['get', 'post'], detail=True)
    # def unsubscribe(self, request, author=None):
    #     if request.method == 'POST':
    #         sub = Subscription.objects.get(author=author, follower=request.auth.user)

    #         try:
    #             subscription = Subscription()
    #             subscription.ended_on = date.today()
    #             subscription.save()

    #             return Response({}, status=status.HTTP_201_CREATED)

        
    #     # If the client performs a request with a method of
    #     # anything other than POST or DELETE, tell client that
    #     # the method is not supported
    #     return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)





class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'created_on', 'ended_on', 'author', 'follower')
        # depth = 1