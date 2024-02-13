from rest_framework import serializers
from django.contrib.auth.hashers import make_password,check_password

from account.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
            'email',
            'phone_number',
            'password'
        )


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username", "full_name", "email", "phone_number", "password",
        )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
