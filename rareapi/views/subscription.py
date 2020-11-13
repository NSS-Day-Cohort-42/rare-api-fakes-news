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

    def patch(self, request, pk=None):
        try:
            subscription = Subscription.objects.get(pk=pk)
            subscription.ended_on = date.today()

            serializer = SubscriptionSerializer(subscription, context={'request': request}, partial=True)

            subscription.save()

            return Response(status=status.HTTP_201_CREATED, data=serializer.data)

        except supscription.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)



class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'created_on', 'ended_on', 'author', 'follower')
        # depth = 1