from django.urls import path
from .views import CreateAccountView, ProfileView

app_name = "accounts"

urlpatterns = [
    path("create-account/", CreateAccountView.as_view(), name="createAccount"),
    path("in/<str:slug>/", ProfileView.as_view(), name="profile"),
]
