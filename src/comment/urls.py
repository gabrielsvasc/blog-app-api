"""URL's da rota de Comentários da API."""
from django.urls import path, include

from rest_framework.routers import DefaultRouter, Route

from comment import views


router_public = DefaultRouter()

router_public.register('', views.CommentViewSet)

app_name = 'comment'

urlpatterns = [
    path('', include(router_public.urls)),
]
