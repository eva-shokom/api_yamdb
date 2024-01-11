from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets, permissions, status, pagination, filters)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Categories, Genres, Title, Review
from users.models import User
from .serializers import (
    CategoriesSerializer, GenresSerializer, TitleReadSerializer,
    ReviewSerializer, CommentSerializer, SignUpSerializer,
    TokenSerializer, UserSerializer, TitleWriteSerializer
)
from .permissions import (
    IsAuthorOrAdminOrModeratorOrReadOnly,
    IsAdmin,
    IsAdminOrReadOnly,
)
from .utils import (send_confirmation_email)
from .filters import TitleFilter
from .viewsets import BaseViewSet


class SignUpViewSet(APIView):
    """Регистрация нового пользователя."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Отправляет код подтверждения на email.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            return Response(
                'Такой логин или email уже существуют',
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            confirmation_code = default_token_generator.make_token(user)
            send_confirmation_email(user, confirmation_code)
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )


class TokenViewSet(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        return Response(
            'Неверный код подтверждения',
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    search_fields = ['username']
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [filters.SearchFilter]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = SignUpSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            if 'role' in serializer.validated_data:
                serializer.validated_data.pop('role')
            serializer.save()
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )

        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(BaseViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenreViewSet(BaseViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModeratorOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModeratorOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
