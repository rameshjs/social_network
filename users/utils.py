from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


def get_tokens_for_user(email):
    user = User.objects.get(email=email)
    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)
