from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, pagination, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import (
    IsAdmin, IsAuthorOrAdminOrModeratorOrReadOnly, IsAdminOrReadOnly
)
from .serializers import (
    CategoriesSerializer, CommentSerializer, GenresSerializer,
    ReviewSerializer, SignUpSerializer, TitleReadSerializer,
    TitleWriteSerializer, TokenSerializer, UserSerializer,
    UserSerializerOrReadOnly
)
from .viewsets import BaseViewSet
from reviews.models import Categories, Genres, Review, Title
from users.models import User


class SignUpViewSet(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Отправляет код подтверждения на email."""

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user_by_email = User.objects.filter(email=email).first()
        user_by_username = User.objects.filter(username=username).first()
        if (
            user_by_email and user_by_username
            and user_by_email != user_by_username
        ):
            return Response(
                {
                    "username": [
                        "Пользователь с таким username уже существует."
                    ],
                    "email": [
                        "Пользователь с таким email уже существует."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST)
        if user_by_email and not user_by_username:
            return Response(
                {
                    "email": [
                        "Пользователь с таким email уже существует."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST)
        if user_by_username and not user_by_email:
            return Response(
                {
                    "username": [
                        "Пользователь с таким username уже существует."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST)
        user, is_created = User.objects.get_or_create(
            email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Ваш код подтверждения:',
            message=f'Код подтверждения - "{confirmation_code}".',
            from_email=settings.ADMIN_EMAIL,
            recipient_list=[email]
        )
        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK)


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
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
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
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        serializer = UserSerializerOrReadOnly(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        if self.action in ('list', 'retrieve'):
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
