from django.contrib import admin
from django.urls import path
from core.views import home, register, desafio, leaderboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', home, name="home"),
    path('desafio/', desafio, name='desafio'),

    # Auth padrão Django
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('top/', leaderboard, name="leaderboard"),

    # Cadastro (custom)
    path('register/', register, name='register'),
]