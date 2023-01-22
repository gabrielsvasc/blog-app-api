"""URL's da rota de Comentários da API."""
from django.urls import path, include

from rest_framework.routers import DefaultRouter, Route

from comment import views


router = DefaultRouter()

router.register('', views.CommentViewSet)

app_name = 'comment'

urlpatterns = [
    path('', include(router.urls)),
]
