from typing import Any
from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.auth.hashers import make_password
from django.apps import apps


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: str | None = ...,
        username: str | None = None,
        **extra_fields: Any
    ) -> Any:
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str | None,
        username: str | None = None,
        **extra_fields: Any
    ) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
