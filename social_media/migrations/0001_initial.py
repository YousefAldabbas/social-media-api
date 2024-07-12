# Generated by Django 4.2.7 on 2024-07-12 23:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import social_media.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=social_media.models.social_media_image_file_path,
                    ),
                ),
                ("hashtag", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ManyToManyField(
                        related_name="posts", to="social_media.category"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="social_media.post",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("content", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=social_media.models.social_media_image_file_path,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="social_media.post",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
