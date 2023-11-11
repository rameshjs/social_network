from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), lookup="iexact")],
    )
    password = serializers.CharField(required=True, min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
