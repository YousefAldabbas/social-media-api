from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import UserFollowing


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "lives_in",
            "birthday",
            "bio",
            "date_of_joining",
            "is_staff",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserListSerializer(UserSerializer):
    num_following = serializers.IntegerField(read_only=True)
    num_followers = serializers.IntegerField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "lives_in",
            "birthday",
            "bio",
            "date_of_joining",
            "is_staff",
            "num_following",
            "num_followers",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5}}


class UserDetailSerializer(UserSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "lives_in",
            "birthday",
            "bio",
            "date_of_joining",
            "is_staff",
            "following",
            "followers",
        )

    def get_following(self, obj):
        return UserFollowingSerializer(
            obj.following.all(),
            many=True,
        ).data

    def get_followers(self, obj):
        return UserFollowersSerializer(
            obj.followers.all(),
            many=True,
        ).data


class UserFollowingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source="user_following.id")
    first_name = serializers.ReadOnlyField(
        source="user_following.first_name",
    )
    last_name = serializers.ReadOnlyField(
        source="user_following.last_name",
    )

    class Meta:
        model = UserFollowing
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class UserFollowersSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(
        source="user_id.first_name",
    )
    last_name = serializers.ReadOnlyField(
        source="user_id.last_name",
    )

    class Meta:
        model = UserFollowing
        fields = ("user_id", "first_name", "last_name")
