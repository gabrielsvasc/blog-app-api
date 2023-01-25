"""URL's da rota de Posts da API."""

from django.urls import path, include
from post.routers import PostRouter
from post import views


router = PostRouter()

router.register('', views.PostViewSet, basename='post')

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]
