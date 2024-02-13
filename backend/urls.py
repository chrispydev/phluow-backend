from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user-auth/", include("account.urls")),
    path("company-auth/", include("company.urls")),
]

