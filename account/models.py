from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # def create_superuser(self, phone_number, password, **extra_fields):
    #     extra_fields.setdefault("is_staff", True)
    #     extra_fields.setdefault("is_superuser", True)

    #     if extra_fields.get("is_staff") is not True:
    #         raise ValueError("Superuser must have is_staff set to True")

    #     if extra_fields.get("is_superuser") is not True:
    #         raise ValueError("Superuser must have is_superuser set to True")

    #     return self.create_user(phone_number=phone_number, password=password, **extra_fields)


class User(AbstractUser):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    # Add related_name arguments to avoid clashes with the default User model
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.phone_number.as_e164