from django.urls import path
from .views import CreateAccountView, ProfileView, CustomUserListView

app_name = "accounts"

urlpatterns = [
    path("create_account/", CreateAccountView.as_view(), name="create_account"),
    path("list/", CustomUserListView.as_view(), name="user_list"),
    path("in/<str:slug>/", ProfileView.as_view(), name="profile"),
]
