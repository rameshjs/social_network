from django.urls import path
from . import views

urlpatterns = [
    path("sign_up", views.sign_up, name="sign_up"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("send_friend_request", views.send_friend_request, name="send_friend_request"),
    path("friends", views.friends, name="friends"),
    path("all_users", views.all_users, name="all_users"),
    path(
        "pending_friend_request",
        views.pending_friend_request,
        name="pending_friend_request",
    ),
    path(
        "accept_friend_request/<int:request_id>",
        views.accept_friend_request,
        name="accept_friend_request",
    ),
    path(
        "reject_friend_request/<int:request_id>",
        views.reject_friend_request,
        name="reject_friend_request",
    ),
]
