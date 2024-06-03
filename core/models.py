import uuid
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # This method will return the currently active user model


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_id = models.IntegerField()
    profile_image = models.ImageField(upload_to='profile_images', default='blank_profile')
    Bio = models.TextField(blank=True)
    location = models.CharField(max_length=20, blank=True)
    followers = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# are you able to see?
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    createdAt = models.DateTimeField(default=datetime.now)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class LikePost(models.Model):
    username = models.CharField(max_length=100)
    post_id = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Followers(models.Model):
    user = models.CharField(max_length=100)
    follower = models.CharField(max_length=100)

    def __str__(self):
        return self.user
