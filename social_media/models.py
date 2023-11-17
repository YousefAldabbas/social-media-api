import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


def social_media_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "social_media", filename)


class Category(models.Model):
    name = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        "user.User",
        null=True,
        related_name="posts",
        on_delete=models.CASCADE,
    )
    created_at = models.DateField(
        auto_now_add=True,
    )
    category = models.ManyToManyField(
        Category,
        related_name="posts",
    )
    title = models.CharField(
        max_length=255,
    )
    content = models.TextField()
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=social_media_image_file_path,
    )
    hashtag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        "user.User",
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateField(
        auto_now_add=True,
    )
    content = models.TextField()
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=social_media_image_file_path,
    )

    class Meta:
        ordering = ["-created_at"]


class Like(models.Model):
    created_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )
