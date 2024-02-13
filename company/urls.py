from django.urls import path, include

from company.views import SignUpView, AccountView, LoginView

urlpatterns = [
    path('', AccountView.as_view(), name='users'),
    path("signup/", SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]

