from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.models import Categories, Genres, Title, Review, Comment
from users.models import User


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
