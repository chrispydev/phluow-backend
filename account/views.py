from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.core.mail import send_mail
import random
import string

from account.models import User
from account.serializers import SignUpSerializer, AccountSerializer


class AccountView(ListAPIView):
    serializer_class = AccountSerializer
    queryset = User.objects.all()


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        data = request.data
        print(data)
        phone_number = data.get("phone_number")

        if phone_number and phone_number.isdigit() and len(phone_number) == 10:
            phone_number = "+233" + phone_number[1:]

        # Update the phone_number value in the data dictionary
        data["phone_number"] = phone_number

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        if phone_number and phone_number.isdigit() and len(phone_number) == 10:
            phone_number = "+233" + phone_number[1:]

        # Generate a unique 5-digit code
        code = self.generate_code()

        # Find the user based on the phone number
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Check if the provided password matches the stored password
        if check_password(password, user.password):
            login(request, user)
            serializer = AccountSerializer(user)
            try:
                self.send_email(user.email, code)
            except Exception as e:
                print(e)
            return Response({"code": code, "data": serializer.data})
        else:
            return Response(
                {"error": "Invalid credentials 2"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def generate_code(self):
        code = "".join(random.choices(string.digits, k=5))
        # Add logic to check if the generated code is unique here
        # For example, you can query the database to ensure the code doesn't exist
        # If the code is not unique, regenerate the code
        return code

    def send_email(self, email, code):
        subject = "Verification Code"
        message = f"Your verification code is: {code}"
        sender = "christianowusu44@gmail.com"
        recipient = email
        send_mail(subject, message, sender, [recipient])
