"""URL's da rota de Tags da API."""
from django.urls import path, include
from tag.routers import TagRouter
from tag import views


router = TagRouter()

router.register('', views.TagViewSet, basename='tag')

app_name = 'tag'

urlpatterns = [
    path('', include(router.urls))
]
