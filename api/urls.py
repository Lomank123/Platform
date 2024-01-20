from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("token/", include("authentication.urls")),
]
