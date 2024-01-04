from rest_framework import serializers
from reviews.models import Categories, Genres, Title, Review, Comment, User

from constants import USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH


class UserSerializer(serializers.ModelSerializer):

    class Mera:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]


class SignUpSerializer(UserSerializer):

    username = serializers.CharField(
        validators=User.user_validators,
        max_length=USERNAME_MAX_LENGTH
    )
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH,
    )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=User.user_validators,
        max_length=USERNAME_MAX_LENGTH
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']

        
class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = CategoriesSerializer(many=False, read_only=True)
    genre = GenresSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
