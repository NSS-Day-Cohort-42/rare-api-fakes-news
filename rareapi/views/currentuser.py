"""Rare User Views Module"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareapi.models import RareUser
from rareapi.views.rareuser import RareUserSerializer

class CurrentUser(ViewSet):
    """RareUser Class"""

    def list(self, request):
        """ handles GET currently logged in user """

        user = RareUser.objects.get(user=request.auth.user)

        serializer = RareUserSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)

