from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth import login, logout
from .forms import ProfileForm, SignupForm, LoginForm
from .forms import ProfileForm
from .forms import ProfileForm, DirectMessageForm
from posts.models import Post
from .models import DirectMessage, Follow, User
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
def user_profile(request, username):
    """
    Profil public d'un autre utilisateur.
    Montre ses posts, events + DM panel.
    """
    user_obj = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=user_obj).order_by('-created_at')
    events = Event.objects.filter(created_by=user_obj).order_by('-start_at')

    is_self = (user_obj == request.user)

    dm_messages = None
    dm_form = None

    if not is_self:
        # vue de l'abonnement
        is_following = Follow.objects.filter(
            follower=request.user,
            followed=user_obj
        ).exists()

        # conversation entre les 2
        dm_messages = DirectMessage.objects.filter(
            Q(sender=request.user, receiver=user_obj)
            | Q(sender=user_obj, receiver=request.user)
        ).order_by("created_at")
        dm_form = DirectMessageForm()

    context = {
        "user_obj": user_obj,
        "posts": posts,
        "events": events,
        "is_self": is_self,
        "dm_messages": dm_messages,
        "dm_form": dm_form,
        "is_following": is_following,
    }
    return render(request, "users/my_profile.html", context)


@login_required
def profile(request):
    """
    Page pour modifier SON propre profil (username + photo).
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
    """
    Mon profil perso : mes posts + mes événements.
    Pas de messagerie ici.
    """
    user = request.user

    posts = Post.objects.filter(author=user).order_by('-created_at')
    events = Event.objects.filter(created_by=user).order_by('-start_at')

    context = {
        "user_obj": user,
        "posts": posts,
        "events": events,
        "is_self": True,
        # pas de DM ici
    }
    return render(request, "users/my_profile.html", context)

@login_required
def send_direct_message(request, username):
    receiver = get_object_or_404(User, username=username)

    if receiver == request.user:
        messages.error(request, "Tu ne peux pas t'envoyer un message à toi-même.")
        return redirect("users:my_profile")

    if request.method == "POST":
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            DirectMessage.objects.create(
                sender=request.user,
                receiver=receiver,
                content=form.cleaned_data["content"],
            )
            messages.success(request, "Message envoyé.")
        else:
            messages.error(request, "Message invalide.")
    return redirect("users:user_profile", username=receiver.username)

@login_required
def messages_view(request, username=None):
    """
    Page Messages :
      - /messages/ : liste des conversations
      - /messages/<username>/ : liste + conversation avec <username>
    """
    user = request.user

    # Tous les messages où je suis impliqué
    all_msgs = DirectMessage.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).select_related("sender", "receiver").order_by("created_at")

    # Construire la liste des conversations (1 entrée par autre utilisateur)
    convo_map = {}
    for msg in all_msgs:
        other = msg.receiver if msg.sender == user else msg.sender
        if other not in convo_map or msg.created_at > convo_map[other].created_at:
            convo_map[other] = msg

    conversations = sorted(
        [{"user": u, "last_message": m} for u, m in convo_map.items()],
        key=lambda d: d["last_message"].created_at,
        reverse=True,
    )

    active_user = None
    thread_messages = None
    dm_form = None

    # Si /messages/<username>/ → conversation active
    if username is not None:
        active_user = get_object_or_404(User, username=username)

        # On évite la conversation avec soi-même
        if active_user == user:
            active_user = None
        else:
            # Messages avec ce user
            thread_messages = DirectMessage.objects.filter(
                Q(sender=user, receiver=active_user)
                | Q(sender=active_user, receiver=user)
            ).order_by("created_at")

            if request.method == "POST":
                dm_form = DirectMessageForm(request.POST)
                if dm_form.is_valid():
                    DirectMessage.objects.create(
                        sender=user,
                        receiver=active_user,
                        content=dm_form.cleaned_data["content"],
                    )
                    return redirect("users:messages_with", username=active_user.username)
            else:
                dm_form = DirectMessageForm()

    context = {
        "conversations": conversations,
        "active_user": active_user,
        "thread_messages": thread_messages,
        "dm_form": dm_form,
    }
    return render(request, "users/messages.html", context)

@login_required
def follow_user(request, username):
    """
    Suivre un autre utilisateur.
    """
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow != request.user:
        Follow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
        )
    return redirect("users:user_profile", username=username)


@login_required
def unfollow_user(request, username):
    """
    Se désabonner d'un utilisateur.
    """
    user_to_unfollow = get_object_or_404(User, username=username)

    Follow.objects.filter(
        follower=request.user,
        followed=user_to_unfollow
    ).delete()

    return redirect("users:user_profile", username=username)
