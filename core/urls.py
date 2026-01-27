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

    path('', views.EntranceListView.as_view(), name='main'),
    path('add/', views.EntranceCreateView.as_view(), name='add'),
    path('search/', views.EntrancesByCPFView.as_view(), name='search'),
    path('client-detail/', views.ClientDetailView.as_view(), name='client-detail'),
    path('cancel/<int:pk>/', views.EntranceSoftDeleteView.as_view(), name='entrance-cancellation')
]