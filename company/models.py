from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import random
import string


class CompanyManager(BaseUserManager):
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


class Company(AbstractUser):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    description = models.TextField(default="This is a text")

    objects = CompanyManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    # Add related_name arguments to avoid clashes with the default User model
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="custom_company_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_company_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.phone_number.as_e164


class Driver(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    driver_number = models.CharField(max_length=10, unique=True, null=False)
    quantity = models.CharField(max_length=1000, default="1")


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True, null=False)
    price = models.CharField(max_length=20, null=False)
    product_image = models.ImageField(upload_to="media_file", default="default.jpg")


class Resource(models.Model):
    products = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="products"
    )
    drivers = models.ForeignKey(
        Driver, related_name="drivers", on_delete=models.CASCADE
    )
