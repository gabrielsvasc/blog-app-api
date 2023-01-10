"""URL's da rota de Posts da API."""

from django.urls import path, include

from rest_framework.routers import DefaultRouter, Route, DynamicRoute

from post import views


class PostPrivateRouter(DefaultRouter):
    """Router utilizado para o mapeamento das rotas privadas."""
    routes = [
        Route(
            url=r'^{prefix}/publish$',
            mapping={'post': 'publish'},
            name='{basename}-publish',
            detail=False,
            initkwargs={}
            # 'suffix': 'Create'
        ),
        Route(
            url=r'^{prefix}/update/{lookup}$',
            mapping={'patch': 'update_post'},
            name='{basename}-update',
            detail=True,
            initkwargs={}
            # 'suffix': 'Detail'
        ),
    ]


router_public = DefaultRouter()
router_private = PostPrivateRouter()

router_public.register('', views.PostPublicViewSet, basename='public')
router_private.register('', views.PostPrivateViewSet, basename='private')

app_name = 'post'

urlpatterns = [
    path('', include(router_public.urls)),
    path('', include(router_private.urls)),
]
