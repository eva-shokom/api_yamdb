from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import(
    CategoryViewSet, CommentViewSet, GenreViewSet, TitleViewSet,
    ReviewViewSet, TokenView, SignUpView, UsersViewSet,
)


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment',
)
v1_router.register(r'users', UsersViewSet, basename='users')

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
    path('v1/', include(v1_router.urls)),
]
