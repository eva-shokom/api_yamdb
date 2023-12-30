from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import(
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    TokenView,
    SignUpView,
    UsersViewSet,
)

router_v1 = DefaultRouter()
router_v1.register(
    r'users',
    UsersViewSet,
    basename='users'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)

auth_urls = [
    path(
        'signup/',
        SignUpView.as_view(),
        name='signup'
    ),
    path(
        'token/',
        TokenView.as_view(),
        name='token'
    )
]


urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls))
]
