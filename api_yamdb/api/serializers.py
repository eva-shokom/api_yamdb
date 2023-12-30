from rest_framework import serializers
from user.models import User

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
        max_length = USERNAME_MAX_LENGTH
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
