from django.urls import path
from . import views

urlpatterns = [
    path("sign_up", views.sign_up, name="sign_up"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("send_friend_request", views.send_friend_request, name="send_friend_request"),
    path(
        "pending_friend_request",
        views.pending_friend_request,
        name="pending_friend_request",
    ),
]
