from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "id",
            "country",
            "city",
        )


class UserSerializer(serializers.ModelSerializer):
    lives_in = LocationSerializer(
        many=False,
        read_only=True,
    )

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


class UserListSerializer(UserSerializer):
    lives_in = LocationSerializer(
        many=False,
        read_only=True,
    )

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


class UserDetailSerializer(UserSerializer):
    lives_in = LocationSerializer(
        many=False,
        read_only=True,
    )

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


