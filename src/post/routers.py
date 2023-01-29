from rest_framework.routers import DefaultRouter, Route


class PostRouter(DefaultRouter):
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
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-retrieve',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/publish/$',
            mapping={'post': 'publish'},
            name='{basename}-publish',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/update/{lookup}$',
            mapping={'patch': 'update_post'},
            name='{basename}-update',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/delete/{lookup}$',
            mapping={'delete': 'delete_post'},
            name='{basename}-delete',
            detail=True,
            initkwargs={}
        )
    ]
