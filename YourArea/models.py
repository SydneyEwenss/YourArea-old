from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from colorfield.fields import ColorField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = ProcessedImageField(default='images/default-avatar.jpg', upload_to='images/', processors=[ResizeToFill(500, 500)], format='JPEG', options={'quality': 60})
    display_name = models.CharField(null=True, blank=True, max_length=150)
    profile_bio = models.CharField(null=True, blank=True, max_length=180)
    background_image = ProcessedImageField(null=True, blank=True, upload_to='images/', processors=[ResizeToFill(1920, 1080)], format='JPEG', options={'quality': 60})

    favourite_colour = ColorField(default="#FFFFFF")

    spotify_id = models.CharField(null=True, blank=True, max_length=180)

    youtube_link = models.CharField(null=True, blank=True, max_length=180)
    twitch_link = models.CharField(null=True, blank=True, max_length=180)
    tiktok_link = models.CharField(null=True, blank=True, max_length=180)
    instagram_link = models.CharField(null=True, blank=True, max_length=180)
    custom_link = models.CharField(null=True, blank=True, max_length=180)

    general_interests = models.CharField(null=True, blank=True, max_length=500)
    music_interests = models.CharField(null=True, blank=True, max_length=500)
    television_interests = models.CharField(null=True, blank=True, max_length=500)
    movies_interests = models.CharField(null=True, blank=True, max_length=500)
    books_interests = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = Profile(user=instance)
            user_profile.save()
            user_profile.follows.set([instance.profile.id])
            user_profile.save()

class Post(models.Model):
    user = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE
    )
    body = models.CharField(max_length=1000, null=True, blank=True)
    post_image = ProcessedImageField(null=True, blank=True, upload_to='images/post_photos', processors=[], format='JPEG', options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_like')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_at').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )

class Notification(models.Model):
    #1 = like, 2 = comment, 3 = follow
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user_has_seen = models.BooleanField(default=False)