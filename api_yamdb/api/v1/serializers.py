from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from reviews.models import Categories, Genres, Title, Review, Comment
from users.models import User

from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]


class SignUpSerializer(UserSerializer):
    """Сериализатор для регистрации."""
    username = serializers.CharField(max_length=150,
                                     validators=User.user_validators,
                                     required=True)
    email = serializers.EmailField(max_length=150,
                                   required=True)


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для аутентификации по токену."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    lookup_field = 'slug'

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    lookup_field = 'slug'

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.now().year),
        ],
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Categories.objects.all()
    )

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title

    def to_representation(self, value):
        return TitleReadSerializer(value).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if self.context['request'].method == 'POST' and Review.objects.filter(
            author=author, title_id=title_id
        ).exists():
            raise ValidationError('Вы уже оставили отзыв на это произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
