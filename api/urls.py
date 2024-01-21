from django.urls import path, include

from api.views import TestView


app_name = "api"

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("test/", TestView.as_view(), name="test"),
]
