from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('mon-profil/', views.my_profile, name='my_profile'),
    path('profil/<str:username>/', views.user_profile, name='user_profile'),
    path('profil/<str:username>/message/', views.send_direct_message, name='send_message'),

    # 🔽 nouvelle page Messages
    path('messages/', views.messages_view, name='messages'),
    path('messages/<str:username>/', views.messages_view, name='messages_with'),

    # gestion des abonnés
    path("follow/<str:username>/", views.follow_user, name="follow_user"),
    path("unfollow/<str:username>/", views.unfollow_user, name="unfollow_user"),
]
