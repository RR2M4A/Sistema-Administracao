from django.urls import path
from .forms import LoginForm
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'
urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='core/auth/login.html',
            authentication_form=LoginForm,
        ),
        name='login',
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='core/auth/logout.html'),
        name='logout',
    ),
]