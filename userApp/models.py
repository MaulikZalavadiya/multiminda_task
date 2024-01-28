import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class ApplicationUser(AbstractBaseUser, PermissionsMixin):
    role_choices = [
        ("admin", "admin"),
        ("user", "user"),
    ]
    role = models.CharField(max_length=10, choices=role_choices, default="user")
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        unique=True,
        help_text=_(
            "Required. A 32 hexadecimal digits number as specified in RFC 4122."
        ),
        error_messages={
            "unique": _("A user with that uuid already exists."),
        },
        default=uuid.uuid4,
    )

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=30,
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ Only."
        ),
        validators=[
            validators.RegexValidator(
                r"^[\w.@+-]+$",
                _(
                    "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."
                ),
            ),
        ],
        error_messages={"unique": _("A user with that username already exists.")},
    )
    first_name = models.CharField(_("First name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("Last name"), max_length=30, blank=True, null=True)

    email = models.EmailField(_("Email address"), unique=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class PasswordResetId(models.Model):
    @staticmethod
    def set_password_reset_expiration_time():
        return timezone.now() + timezone.timedelta(days=1)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(
        default=set_password_reset_expiration_time.__func__
    )

    class Meta:
        verbose_name = "Password reset id"
