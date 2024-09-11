from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.permissions.is_account_owner import IsAccountOwner
from core.permissions.is_super_user_permission import IsSuperUser

from apps.users.serializers import UserSerializer

UserModel = get_user_model()


# --------------------------------------- User views start --------------------------------------------

@method_decorator(name='post', decorator=swagger_auto_schema(security=[], operation_summary='Create user account'))
class UserCreateView(CreateAPIView):
    """Create a new user in the system"""
    permission_classes = (AllowAny,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_summary='Get all users'))
class UserListView(ListAPIView):
    """List all users in the system"""
    permission_classes = (AllowAny,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_summary='Get a specific user'))
class UserRetrieveView(RetrieveAPIView):
    """Retrieve a specific user"""
    permission_classes = (AllowAny,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    """Update a user"""
    permission_classes = (IsAccountOwner,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserDestroyView(DestroyAPIView):
    """Delete user"""
    permission_classes = (IsAdminUser, IsAccountOwner)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserToPremiumView(GenericAPIView):
    """Give user a premium account"""
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def patch(self, *args, **kwargs):
        user = self.request.user

        if not user.is_premium:
            user.is_premium = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class PremiumToUserView(GenericAPIView):
    """Take away a user's premium account"""
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_premium:
            user.is_premium = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


# --------------------------------------- User views end --------------------------------------------

# ----------------------------------------Admin priviliges-------------------------------------
class UserBlockView(GenericAPIView):
    """Block a user"""
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_active:
            user.is_active = False
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserUnBlockView(GenericAPIView):
    """Unblock a user"""
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if not user.is_active:
            user.is_active = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToAdminView(GenericAPIView):
    """Change user's status to admin"""
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUserView(GenericAPIView):
    """Change user's status from admin to simple user'"""
    permission_classes = (IsSuperUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
