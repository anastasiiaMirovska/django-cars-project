from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.dataclasses.user_dataclass import User
from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

from apps.auth.serializers import EmailSerializer, PasswordSerializer
from apps.users.serializers import UserSerializer

UserModel: User = get_user_model()

@method_decorator(name='patch', decorator=swagger_auto_schema(security=[], operation_summary='Authenticate user account'))
class ActivateUserView(GenericAPIView):
    """Activate user account with token"""
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def patch(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[], operation_summary='Send request for recovery '))
class RecoveryPasswordRequestView(GenericAPIView):
    """Recovery password request"""
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        pass

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        EmailService.recovery_email(user)
        return Response({'detail': 'check your email'}, status=status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[], operation_summary='Recover password with given token'))
class RecoverPasswordView(GenericAPIView):
    """Recover password with given token"""
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def get_serializer_class(self):
        pass

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        token = kwargs['token']
        user = JWTService.verify_token(token, RecoveryToken)
        user.set_password(serializer.data['password'])
        user.save()
        return Response({'detail': 'password was changed'}, status=status.HTTP_200_OK)

