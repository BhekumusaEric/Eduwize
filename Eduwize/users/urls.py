from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from . import views
from eduwize_app.forms import CustomUserCreationForm

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
]
