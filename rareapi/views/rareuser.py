"""Rare User Views Module"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareapi.models import RareUser

class RareUsers(ViewSet):
    """RareUser Class"""

    def list(self, request):
        """ handles GET all"""
        users = RareUser.objects.all()

        serializer = RareUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
           
            user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'date_joined')

class RareUserSerializer(serializers.ModelSerializer):
    """Serializer for RareUser Info from a post"""
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'user')