from django.urls import path, include, re_path
from .views import *
import django.conf.urls

app_name = "YourArea"

urlpatterns = [
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("area_list/", profile_list, name="profile_list"),
    path("area/<int:pk>", profile, name="profile"),
    path("area/followers/<int:pk>", followers, name="followers"),
    path("area/following/<int:pk>", following, name="following"),
    path("post/<int:pk>", post, name="post"),
    path("post/<int:post_pk>/comment/<int:pk>/reply", CommentReplyView.as_view(), name="comment_reply"),
    path("post/likes/<int:pk>", likes, name="likes"),
    path("update_area/", update_area, name="update_area"),
    path("post_like/<int:pk>", post_like, name="post_like"),
    path("comment_like/<int:post_pk>/comment/<int:pk>/like", comment_like, name="comment_like"),
    path("delete_post/<int:pk>", delete_post, name="delete_post"),
    path("search/", search, name="search"),
    path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name="post_notification"),
    path('notification/<int:notification_pk>/profile/<int:profile_pk>', FollowNotification.as_view(), name="follow_notification"),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name="notification_delete"),
    re_path(r"^register/", register, name="register"),
]