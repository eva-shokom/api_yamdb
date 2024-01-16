from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import ValidationError
from reviews.models import Categories, Comment, Genres, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации"""

    username = serializers.CharField(max_length=settings.USERNAME_MAX_LENGTH,
                                     validators=User.user_validators)
    email = serializers.EmailField(max_length=settings.EMAIL_MAX_LENGTH)


class TokenSerializer(serializers.Serializer):
    """Сериализатор для аутентификации по токену"""

    username = serializers.CharField(max_length=settings.USERNAME_MAX_LENGTH,
                                     validators=User.user_validators)
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
    rating = serializers.IntegerField(read_only=True, default=None)
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
    year = serializers.IntegerField()
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
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs['title_id']
            author = self.context['request'].user
            if Review.objects.filter(
                    author=author, title_id=title_id).exists():
                raise ValidationError(
                    'Вы уже оставили отзыв на это произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
