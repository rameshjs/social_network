from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        (1, "Pending"),
        (2, "Accepted"),
        (3, "Rejected"),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    sent_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requests_sent"
    )
    sent_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requests_received"
    )
    sent_on = models.DateTimeField(auto_now_add=True)

    def accept_friend_request(self):
        if self.status == 1:  # Check if the request is still pending
            self.status = 2  # Update the status to 'Accepted'
            self.save()

            # Create two-way friendships
            self.sent_from.friends.add(self.sent_to)
            self.sent_to.friends.add(self.sent_from)

    def reject_friend_request(self):
        if self.status == 1:  # Check if the request is still pending
            self.status = 3  # Update the status to 'Rejected'
            self.save()
