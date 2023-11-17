from django.db.models import Count
from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters


from user.models import User, UserFollowing
from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserFollowingSerializer,
)


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["nickname", "lives_in"]

    def get_queryset(self):
        queryset = self.queryset.annotate(
                num_following=Count("following"),
                num_followers=Count("followers"),
            )

        return queryset

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserFollowingView(viewsets.ModelViewSet):
    serializer_class = UserFollowingSerializer
    queryset = UserFollowing.objects.all()


class UserFollow(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, pk):
        user = request.user
        follow = self.get_object(pk)
        UserFollowing.objects.create(
            user_id=user,
            user_following=follow
        )
        serializer = UserSerializer(follow)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = request.user
        follow = self.get_object(pk)
        connection = UserFollowing.objects.filter(
            user_id=user,
            user_following=follow
        ).first()
        connection.delete()
        serializer = UserSerializer(follow)
        return Response(serializer.data)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
