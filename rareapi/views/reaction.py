"""Reaction Views Module"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from django.http import HttpResponseServerError
from rest_framework.response import Response
from rareapi.models import Reaction

class Reactions(ViewSet):
    """Reactions Class"""

    def list(self, request):
        """ handles GET all"""
        reactions = Reaction.objects.all()

        serializer = ReactionSerializer(reactions, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
           
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

   

class ReactionSerializer(serializers.ModelSerializer):
    """ ReactionSerializer """
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')