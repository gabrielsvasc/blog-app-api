"""URL's da rota de Tags da API."""
from django.urls import path, include

from rest_framework.routers import DefaultRouter, Route

from tag import views


class TagPrivateRouter(DefaultRouter):
    """Router utilizado para o mapeamento das rotas privadas."""
    routes = [
        Route(
            url=r'^{prefix}/create/$',
            mapping={'post': 'create'},
            name='{basename}-create',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/delete/{lookup}$',
            mapping={'delete': 'delete'},
            name='{basename}-delete',
            detail=True,
            initkwargs={}
        ),
    ]


router_public = DefaultRouter()
router_private = TagPrivateRouter()

router_public.register('', views.TagPublicViewSet, basename='public')
router_private.register('', views.TagPrivateViewSet, basename='private')

app_name = 'tag'

urlpatterns = [
    path('', include(router_public.urls)),
    path('', include(router_private.urls)),
]
