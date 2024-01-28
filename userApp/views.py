from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from templated_email import send_templated_mail
from .serializers import (
    AuthorizeUserSerializer,
    UserAuthSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
)
from .models import PasswordResetId
from utils.utils import CustomRenderer
from utils.permissions import IsAPIKEYAuthenticated

from .models import ApplicationUser


class UserViewSet(viewsets.GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    queryset = ApplicationUser.objects.all()
    lookup_field = "uuid"
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    renderer_classes = [CustomRenderer]

    def get_serializer_class(self):
        if self.action == "reset_password":
            return PasswordResetSerializer

        return AuthorizeUserSerializer

    @action(
        methods=["post"],
        detail=False,
        permission_classes=[AllowAny, IsAPIKEYAuthenticated],
        url_name="password-reset-email",
        url_path="password_reset_email",
    )
    def password_reset_email(self, request, *args, **kwargs):
        email = request.data.get("email")

        if not email:
            raise ValidationError("Email is required.")

        user = ApplicationUser.objects.filter(email__iexact=email).first()

        if not user:
            raise NotFound("Provided email is not exists.")

        password_reset_obj = PasswordResetId.objects.create(user=user)

        send_templated_mail(
            template_name="reset_password",
            from_email="test@email.com",
            recipient_list=[user.email],
            context={
                "subject": "Reset Password",
                "domain": "127.0.0.1",
                "password_reset_id": password_reset_obj.id,
                "protocol": "https"
                if getattr(settings, "FRONTEND_USE_HTTPS", False)
                else "http",
                "fullname": user.username,
            },
        )
        return Response("Email has been sent.")

    @action(
        methods=["post"],
        detail=False,
        permission_classes=[AllowAny, IsAPIKEYAuthenticated],
        url_path="reset-password/(?P<password_reset_id>.*)",
        url_name="reset_password",
    )
    def reset_password(self, request, *args, **kwargs):
        password_reset_obj = get_object_or_404(
            PasswordResetId,
            pk=self.kwargs.get("password_reset_id"),
            expiration_time__gt=timezone.now(),
        )

        serializer = self.get_serializer_class()(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = ApplicationUser.objects.get(pk=password_reset_obj.user.id)

        user.set_password(serializer.data["password"])
        user.save()

        PasswordResetId.objects.filter(pk=password_reset_obj.pk).delete()

        data = UserAuthViewSet.get_success_header(user)

        return Response(data=data)


class UserAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = "X-Token"
    renderer_classes = [CustomRenderer]

    @classmethod
    def get_success_header(cls, user):
        return {cls.NEW_TOKEN_HEADER: user.user_auth_tokens.create().key}

    @action(
        methods=["post"],
        detail=False,
        permission_classes=[AllowAny, IsAPIKEYAuthenticated],
        url_name="registration",
        url_path="registration",
    )
    def registration(self, request, *args, **kwargs):
        register_serializer = RegisterSerializer(
            data=request.data, context={"request": request, "view": self}
        )
        register_serializer.is_valid(raise_exception=True)
        register_serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=["post"],
        detail=False,
        permission_classes=[AllowAny, IsAPIKEYAuthenticated],
        url_name="login",
        url_path="login",
    )
    def login(self, request, *args, **kwargs):
        auth_serializer = UserAuthSerializer(
            data=request.data, context={"request": request, "view": self}
        )
        auth_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **auth_serializer.data)
        if not user:
            raise NotFound("Invalid credentials.")

        user_details = AuthorizeUserSerializer(
            instance=user, context={"request": request, "view": self}
        ).data
        user_details.update(self.get_success_header(user))

        return Response(data=user_details, status=status.HTTP_200_OK)

    @action(
        methods=["delete"],
        detail=False,
        permission_classes=[IsAuthenticated, IsAPIKEYAuthenticated],
    )
    def logout(self, request, *args, **kwargs):
        if request.user.user_auth_tokens.count() > 1:
            self.request.auth.delete()
        else:
            request.user.user_auth_tokens.all().delete()
        return Response(None, status=status.HTTP_200_OK)
