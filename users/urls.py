from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            email_template_name='users/password_reset_email.txt',
            subject_template_name='users/password_reset_subject.txt',
            success_url=reverse_lazy('users:password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path('signup/', views.signup, name='signup'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
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
