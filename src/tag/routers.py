from rest_framework.routers import DefaultRouter, Route


class TagRouter(DefaultRouter):
    """Router utilizado para o mapeamento das rotas privadas."""
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={}
        ),
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
        Route(
            url=r'^{prefix}/update/{lookup}$',
            mapping={'put': 'update'},
            name='{basename}-update',
            detail=True,
            initkwargs={}
        ),
    ]
