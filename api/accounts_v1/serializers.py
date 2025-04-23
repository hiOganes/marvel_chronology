from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.accounts.utils import check_password


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        # Check email for uniqueness
        if get_user_model().objects.filter(email=value).exists():
            raise ValidationError("Такой E-mail уже существует!")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Пароль короче 8 символов!")
        if not check_password(value):
            raise ValidationError(
                "Пароль должен состоять латинских из букв и цифр"
            )
        return value