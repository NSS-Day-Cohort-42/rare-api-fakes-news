"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category


class Categories(ViewSet):
    """Rare Categories"""

    def list(self, request):
        """Handle GET requests to get all the categories

        Returns:
        Response -- JSON serialized list of categories
        """
        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for event organzier's related Django user"""
    class Meta:
        model = Category
        fields = ['id', 'label']