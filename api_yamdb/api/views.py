from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets, mixins, permissions, status, pagination, filters)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Categories, Genres, Title, Review
from users.models import User
from .serializers import (
    CategoriesSerializer, GenresSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer, SignUpSerializer,
    TokenSerializer, UserSerializer,
)
from .permissions import (
    IsAuthorOrAdminOrModeratorOrReadOnly, IsOwnerOrAdmin, IsAdmin)
from .utils import (
    check_confirmation_code, generate_confirmation_code,
    send_confirmation_email
)


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
            confirmation_code = generate_confirmation_code(user)
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
        if check_confirmation_code(user, confirmation_code):
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
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrAdmin]
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


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModeratorOrReadOnly,
    )

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('post_id'))

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

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('post_id'))

    def get_review(self):
        title = self.get_title()
        return get_object_or_404(
            Review, title=title, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        title = self.get_title()
        review = self.get_review()
        serializer.save(author=self.request.user, title=title, review=review)
