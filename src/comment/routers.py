from rest_framework.routers import DefaultRouter, Route


class CommentRouter(DefaultRouter):
    """Router utilizado para o mapeamento das rotas."""
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
            url=r'^{prefix}/update/{lookup}$',
            mapping={'patch': 'update'},
            name='{basename}-update',
            detail=True,
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
