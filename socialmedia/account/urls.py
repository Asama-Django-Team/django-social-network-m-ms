from django.urls import path
from . import views


app_name = "account"
urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="user_register"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
    path("profile/<int:user_id>", views.UserProfileView.as_view(), name="user_profile"),
    path("community/", views.CommunityView.as_view(), name="user_community")
]