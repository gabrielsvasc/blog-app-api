"""URL's da rota de Tags da API."""
from django.urls import path, include

from rest_framework.routers import DefaultRouter, Route

from tag import views

router_public = DefaultRouter(trailing_slash=False)

router_public.register('', views.TagPublicViewSet, basename='public')

app_name = 'tag'

urlpatterns = [
    path('', include(router_public.urls)),
]
