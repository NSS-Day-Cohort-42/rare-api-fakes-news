"""rareapifakesnews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.urls import path
from rareapi.views import register_user, login_user
from rareapi.views.subscription import Subscriptions
from rareapi.views import Categories, PostReactions, Posts, PostTags, Reactions, Tags, RareUsers, CurrentUser, Subscriptions
from rest_framework import routers
from rareapi.views import Comments


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')
router.register(r'currentuser', CurrentUser, 'rareuser')
router.register(r'postreactions', PostReactions, 'postreaction')
router.register(r'posts', Posts, 'post')
router.register(r'posttags', PostTags, 'posttag')
router.register(r'subscriptions', Subscriptions, 'subscription')
router.register(r'comments', Comments, 'comment')
router.register(r'users', RareUsers, 'rareuser')
router.register(r'reactions', Reactions, 'reaction')
router.register(r'tags', Tags, 'tag')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),

]
