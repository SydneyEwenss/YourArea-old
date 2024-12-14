from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import login
from django.urls import reverse
from django.views import View
from django.http import HttpResponse

def dashboard(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user__id=request.user.id)
        followed_posts = Post.objects.filter(user__id__in=request.user.profile.follows.all().values_list('user_id')).order_by("-created_at")
    else:
        followed_posts = None
    all_posts = Post.objects.all().order_by("-created_at")

    return render(
        request,
        "YourArea/dashboard.html",
        {"posts": all_posts, "followed_posts": followed_posts},
    )

def profile_list(request):
    profiles = Profile.objects.all().order_by("-date_modified")
    return render(request, "YourArea/profile_list.html", {"profiles": profiles})

def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    posts = profile.user.posts.all().order_by("-created_at")

    if request.user.is_authenticated:
        if not hasattr(request.user, 'profile'):
            missing_profile = profile(user=request.user)
            missing_profile.save()

        if request.method == "POST":
            current_user_profile = request.user.profile
            data = request.POST
            action = data.get("follow")
            if action == "follow":
                current_user_profile.follows.add(profile)
                notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)
            elif action == "unfollow":
                current_user_profile.follows.remove(profile)
            current_user_profile.save()

            form = PostForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect("YourArea:profile", current_user_profile.id)
        
    return render(request, "YourArea/profile.html", {"form": PostForm(), "profile": profile, "posts": posts})

def followers(request, pk):
    profiles = Profile.objects.get(user_id=pk)
    return render(request, "YourArea/followers.html", {"profiles": profiles})

def following(request, pk):
    profiles = Profile.objects.get(user_id=pk)
    return render(request, "YourArea/following.html", {"profiles": profiles})

def likes(request, pk):
    post = Post.objects.get(id=pk)
    users = post.likes.all()

    return render(request, "YourArea/likes.html", {"profiles": users})

def update_area(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        # user_form = CustomUserCreationForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfileExtrasForm(request.POST or None, request.FILES or None, instance=profile_user, use_required_attribute=False)
        if profile_form.is_valid():
            # user_form.save()
            profile_form.save()
            # login(request, current_user)
            print("user changed")
            return redirect('YourArea:profile', current_user.profile.id)
        print("user not changed")
        return render(request, "YourArea/update_area.html", {'form': profile_form})
    else:
        return redirect('YourArea:dashboard')

def post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.user, post=post)

    form = CommentForm()

    comments = Comment.objects.filter(post=post).order_by("-created_at")

    return render(
        request,
        "YourArea/post.html",
        {"form": form, "post": post, "comments": comments},
    )

class CommentReplyView(View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('YourArea:post', pk=post_pk)

def register(request):
    if request.method == "GET":
        return render(
            request, "YourArea/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("YourArea:dashboard"))
        else:
            return render(
                request, "YourArea/register.html",
                {"form": CustomUserCreationForm}
            )

def post_like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.user, post=post)
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        return redirect('YourArea:login')

def comment_like(request, pk, *args, **kwargs):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        if comment.likes.filter(id=request.user.id):
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
            # notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.user, post=post)
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        return redirect('YourArea:login')

def delete_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if request.user.username == post.user.username:
            post.delete()
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        return redirect(request.META.get("HTTP_REFERER"))

def search(request):
    if request.method == "POST":
        search = request.POST['search']

        searched = Post.objects.filter(body__contains = search).order_by("-created_at")
        searched_profiles = Profile.objects.filter(user__username__contains = search)

        return render(request, 'YourArea/search.html', {'search': search, 'searched': searched, 'searched_profiles': searched_profiles})
    else:
        return render(request, 'YourArea/search.html', {})

class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('YourArea:post', pk=post_pk)

class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = Profile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('YourArea:profile', pk=profile_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()
        return HttpResponse('Success', content_type='text/plain')