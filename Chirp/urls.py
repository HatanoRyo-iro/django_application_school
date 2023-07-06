from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path('', views.home, name='home'),
]