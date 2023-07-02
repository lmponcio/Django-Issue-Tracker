from django.urls import path
from .views import CreateAccountView, ProfileView, success_login, success_logout

app_name = "accounts"

urlpatterns = [
    path("create-account/", CreateAccountView.as_view(), name="createAccount"),
    path("success_login/", success_login, name="success_login"),  # testing
    path("success_logout/", success_logout, name="success_logout"),  # testing
    path("in/<str:slug>/", ProfileView.as_view(), name="profile"),
]
