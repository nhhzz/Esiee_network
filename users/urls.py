from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),          # Modifier le profil (formulaire)
    path('mon-profil/', views.my_profile, name='my_profile'), # Mon profil perso
    path('profil/<str:username>/', views.user_profile, name='user_profile'),  # Profil public
]
