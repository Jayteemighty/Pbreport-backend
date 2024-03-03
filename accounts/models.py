from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import UserManager
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User


class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=20,
        unique=True,
        null=True,
        blank=False,
        db_index=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("That username is not available"),
        },
    )

    email = models.EmailField(
        _("email address"),
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        error_messages={
            "unique": _("That email is not available"),
        },
    )
    first_name = models.CharField(
        _("first name"), max_length=100, null=False, blank=False
    )
    last_name = models.CharField(
        _("last name"), max_length=100, null=False, blank=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        "username",
        "first_name",
        "last_name",
    )

    objects = UserManager()

    # Add related_name attributes to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_groups'  # Example related name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permissions'  # Example related name
    )


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()

    def set_expiry_time(self):
        # Set the expiry time to be, for example, 5 minutes from the current time
        self.expiry_time = timezone.now() + timedelta(minutes=5)
