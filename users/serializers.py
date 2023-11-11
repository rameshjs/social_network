from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

# Models
from users.models import FriendRequest

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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        return user


"""
Serializer for handling friend requests.
validate(data): Custom validation method to check if the sender and receiver are valid for a friend request.
create(validated_data): Method to create a friend request object in the database.
"""


class FriendRequestSerializer(serializers.Serializer):
    sent_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        sent_from_user = self.context["request"].user
        sent_to_user = data["sent_to"]

        # User cant add themselves as a friend.
        if sent_from_user == sent_to_user:
            raise serializers.ValidationError(
                "Cannot send a friend request to yourself."
            )

        existing_request = FriendRequest.objects.filter(
            sent_from=sent_from_user,
            sent_to=sent_to_user,
            status=FriendRequest.STATUS_CHOICES[0][0],
        ).first()

        if existing_request:
            raise serializers.ValidationError("Friend request already sent.")

        return data

    def create(self, validated_data):
        sent_to_user = validated_data["sent_to"]
        sent_from_user = self.context["request"].user

        friend_request = FriendRequest.objects.create(
            sent_to=sent_to_user, sent_from=sent_from_user
        )

        return friend_request


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
        ]


class PendingFriendRequestSerializer(serializers.ModelSerializer):
    sent_from = UserSerializer()
    sent_to = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ["id", "sent_from", "sent_to", "status", "sent_on"]
        read_only_fields = ["id", "sent_on"]


class UserSerializerWithFriends(UserSerializer):
    friends = UserSerializer(many=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + [
            "friends",
        ]
