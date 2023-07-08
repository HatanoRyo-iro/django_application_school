from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path('', views.home, name='home'),
    path('<int:page>/', views.home, name='home'),
    path('groups/', views.groups, name='groups'),
    path('add/',views.add, name='add'),
    path('create_group/', views.create_group, name='create_group'),
    path('post', views.post, name='post'),
    path('share/<int:shared_id>/', views.share, name='share'),
    path('good/<int:good_id>/', views.good, name='good'),
]