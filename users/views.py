from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

# Utils
from users.utils import get_tokens_for_user

# Serializers
from users.serializers import (
    SignUpSerializer,
    LoginSerializer,
    FriendRequestSerializer,
    PendingFriendRequestSerializer,
)

# Models
from users.models import FriendRequest


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        token = get_tokens_for_user(serializer.data["email"])
        return Response({"token": token}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def send_friend_request(request):
    serializer = FriendRequestSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def pending_friend_request(request):
    friend_requests = FriendRequest.objects.filter(sent_to=request.user)
    serializer = PendingFriendRequestSerializer(friend_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest,
        sent_to=request.user,
        pk=request_id,
        status=FriendRequest.STATUS_CHOICES[0][0],
    )
    friend_request.accept_friend_request()
    serializer = PendingFriendRequestSerializer(friend_request)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest,
        sent_to=request.user,
        pk=request_id,
        status=FriendRequest.STATUS_CHOICES[0][0],
    )
    friend_request.reject_friend_request()
    serializer = PendingFriendRequestSerializer(friend_request)
    return Response(serializer.data, status=status.HTTP_200_OK)
