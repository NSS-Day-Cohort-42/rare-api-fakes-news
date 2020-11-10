from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rareapi.views import Posts

"""Router"""
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', Posts, 'post')


urlpatterns = [
    path('', include(router.urls))
]
