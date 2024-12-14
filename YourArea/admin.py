from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile, Post, Comment, Notification

class ProfileInline(admin.StackedInline):
    model = Profile

class CommentInline(admin.StackedInline):
    model = Comment

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "password", "email"]
    inlines = [ProfileInline]

class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [CommentInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Post, PostAdmin)
admin.site.register(Notification)