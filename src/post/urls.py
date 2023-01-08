"""URL's da rota de Posts da API."""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from post import views

router = DefaultRouter()
router.register('', views.PostPrivateViewSet, basename='private')
router.register('', views.PostPublicViewSet, basename='public')

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]
