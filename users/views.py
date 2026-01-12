from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm, ProfileForm
from posts.models import Post
from events.models import Event


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
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect("users:my_profile")  # ou "users:profile" si tu préfères rester sur la page
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