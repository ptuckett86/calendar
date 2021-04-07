from django.db import models
from uuid import uuid4
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager


class MetaModel(models.Model):
    """
    Provides information common to most every object in the database.
    """

    uuid = models.UUIDField(
        default=uuid4, editable=False, db_index=True, unique=True, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class AuthUser(MetaModel, AbstractBaseUser):
    jwt_secret = models.UUIDField(default=uuid4)
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField(_("first name"), max_length=30, null=True)
    last_name = models.CharField(_("last name"), max_length=30, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    suffix = models.CharField(max_length=100, null=True)
    alias = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ["email"]

    @property
    def full_name(self):
        return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)

    def create_user(password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = BaseUserManager().normalize_email(extra_fields.get("email"))
        extra_fields["email"] = email
        user, created = AuthUser.objects.get_or_create(**extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user
