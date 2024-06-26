from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet,
    SignUpViewSet, TitleViewSet, TokenViewSet, UsersViewSet
)


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
v1_router.register('users', UsersViewSet, basename='users')

auth_urls = [
    path(
        'signup/',
        SignUpViewSet.as_view(),
        name='signup'
    ),
    path(
        'token/',
        TokenViewSet.as_view(),
        name='token'
    )
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(v1_router.urls))
]
