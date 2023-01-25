"""URL's da rota de Comentários da API."""
from django.urls import path, include
from comment.routers import CommentRouter
from comment import views


router = CommentRouter()

router.register('', views.CommentViewSet)

app_name = 'comment'

urlpatterns = [
    path('', include(router.urls)),
]
