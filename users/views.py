from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import ProfileForm
from posts.models import Post
from events.models import Event

User = get_user_model()


def home(request):
    return render(request, 'users/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            messages.success(request, "Bienvenue ! Votre compte a été créé.")
            return redirect('users:profile')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('users:profile')
        else:
            messages.error(request, "Identifiants invalides.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('users:home')

@login_required
def my_profile(request):
    """
    Mon profil perso : mes posts + mes événements.
    """
    user = request.user

    posts = Post.objects.filter(author=user).order_by('-created_at')
    events = Event.objects.filter(created_by=user).order_by('-start_at')

    context = {
        "user_obj": user,
        "posts": posts,
        "events": events,
        "is_self": True,
    }
    return render(request, "users/my_profile.html", context)

@login_required
def user_profile(request, username):
    """
    Profil public d'un utilisateur (vu depuis posts/événements).
    """
    user_obj = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=user_obj).order_by('-created_at')
    events = Event.objects.filter(created_by=user_obj).order_by('-start_at')

    context = {
        "user_obj": user_obj,
        "posts": posts,
        "events": events,
        "is_self": (user_obj == request.user),
    }
    return render(request, "users/my_profile.html", context)


@login_required
def profile(request):
    """
    Page pour modifier SON propre profil (username + photo de profil).
    Accessible via le bouton 'Modifier le profil'.
    """
    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect("users:my_profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form})

@login_required
def my_profile(request):
    user = request.user

    # Tous les posts créés par l'utilisateur
    posts = Post.objects.filter(author=user).order_by('-created_at')

    # Tous les événements créés par l'utilisateur
    events = Event.objects.filter(created_by=user).order_by('-start_at')

    context = {
        "user_obj": user,
        "posts": posts,
        "events": events,
    }
    return render(request, "users/my_profile.html", context)