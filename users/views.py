from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import ProfileForm, SignupForm, LoginForm, DirectMessageForm
from posts.models import Post
from .models import DirectMessage, Follow, User
from events.models import Event

User = get_user_model()


def _send_verification_email(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verify_url = request.build_absolute_uri(
        reverse("users:verify_email", kwargs={"uidb64": uidb64, "token": token})
    )

    subject = "Confirme ton inscription ESIEE Network"
    message = (
        f"Bonjour {user.username},\n\n"
        "Merci pour ton inscription sur ESIEE Network.\n"
        "Clique sur le lien ci-dessous pour verifier ton adresse email :\n\n"
        f"{verify_url}\n\n"
        "Si tu n'es pas a l'origine de cette inscription, ignore cet email."
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@esiee-network.local")
    send_mail(subject, message, from_email, [user.email], fail_silently=False)


def home(request):
    return render(request, 'users/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.is_active = False
            user.save()
            try:
                _send_verification_email(request, user)
                messages.success(
                    request,
                    "Compte cree. Un email de verification a ete envoye. "
                    "Confirme ton adresse avant de te connecter.",
                )
            except Exception:
                messages.error(
                    request,
                    "Compte cree, mais l'email de verification n'a pas pu etre envoye. "
                    "Contacte l'administrateur.",
                )
            return redirect('users:login')
        messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def verify_email(request, uidb64, token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
            messages.success(request, "Adresse email verifiee. Tu peux maintenant te connecter.")
        else:
            messages.info(request, "Ce compte est deja verifie.")
    else:
        messages.error(request, "Lien de verification invalide ou expire.")

    return redirect("users:login")


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username", "").strip()
        if username:
            inactive_user = User.objects.filter(
                username__iexact=username,
                is_active=False,
            ).first()
            if inactive_user:
                messages.warning(
                    request,
                    "Compte non active. Verifie d'abord ton adresse email via le lien recu.",
                )
                return render(request, 'users/login.html', {'form': LoginForm(request, data=request.POST)})

        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Connexion reussie.")
            return redirect('users:home')
        messages.error(request, "Identifiants invalides.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "Vous etes deconnecte.")
    return redirect('users:home')


@login_required
def user_profile(request, username):
    """
    Profil public d'un utilisateur (posts + evenements + panel DM).
    """
    user_obj = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=user_obj).order_by('-created_at')
    events = Event.objects.filter(created_by=user_obj).order_by('-start_at')

    is_self = (user_obj == request.user)
    is_following = False

    dm_messages = None
    dm_form = None

    if not is_self:
        is_following = Follow.objects.filter(
            follower=request.user,
            followed=user_obj,
        ).exists()

        dm_messages = DirectMessage.objects.filter(
            Q(sender=request.user, receiver=user_obj)
            | Q(sender=user_obj, receiver=request.user)
        ).order_by('created_at')
        dm_form = DirectMessageForm()

    context = {
        'user_obj': user_obj,
        'posts': posts,
        'events': events,
        'is_self': is_self,
        'dm_messages': dm_messages,
        'dm_form': dm_form,
        'is_following': is_following,
    }
    return render(request, 'users/my_profile.html', context)


@login_required
def profile(request):
    """
    Page pour modifier son propre profil (username + photo).
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis a jour avec succes.")
            return redirect('users:my_profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def my_profile(request):
    """
    Mon profil perso : mes posts + mes evenements.
    """
    user = request.user

    posts = Post.objects.filter(author=user).order_by('-created_at')
    events = Event.objects.filter(created_by=user).order_by('-start_at')

    context = {
        'user_obj': user,
        'posts': posts,
        'events': events,
        'is_self': True,
    }
    return render(request, 'users/my_profile.html', context)


@login_required
def user_search(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.none()

    if query:
        users = (
            User.objects.filter(username__icontains=query)
            .exclude(pk=request.user.pk)
            .order_by("username")[:30]
        )

    context = {
        "query": query,
        "users": users,
    }
    return render(request, "users/user_search.html", context)


@login_required
def send_direct_message(request, username):
    receiver = get_object_or_404(User, username=username)

    if receiver == request.user:
        messages.error(request, "Tu ne peux pas t'envoyer un message a toi-meme.")
        return redirect('users:my_profile')

    if request.method == 'POST':
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            DirectMessage.objects.create(
                sender=request.user,
                receiver=receiver,
                content=form.cleaned_data['content'],
            )
            messages.success(request, "Message envoye.")
        else:
            messages.error(request, "Message invalide.")

    return redirect('users:user_profile', username=receiver.username)


@login_required
def messages_view(request, username=None):
    """
    Page Messages :
      - /messages/ : liste des conversations
      - /messages/<username>/ : liste + conversation active
    """
    user = request.user
    contact_query = request.GET.get("q", "").strip()
    active_user = None
    thread_messages = None
    dm_form = None

    contact_users = User.objects.exclude(pk=user.pk)
    if contact_query:
        contact_users = contact_users.filter(
            Q(username__icontains=contact_query)
            | Q(first_name__icontains=contact_query)
            | Q(last_name__icontains=contact_query)
            | Q(email__icontains=contact_query)
        )
    contact_users = contact_users.order_by("username")[:20]

    # Si /messages/<username>/ -> conversation active
    if username is not None:
        active_user = get_object_or_404(User, username=username)

        # Eviter la conversation avec soi-meme
        if active_user == user:
            active_user = None
        else:
            # Marque comme lus les messages recus depuis cette conversation
            DirectMessage.objects.filter(
                sender=active_user,
                receiver=user,
                is_read=False,
            ).update(is_read=True)

    # Tous les messages ou je suis implique
    all_msgs = DirectMessage.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).select_related('sender', 'receiver').order_by('created_at')

    # Nombre de non lus par expediteur
    unread_counts = {
        row['sender']: row['total']
        for row in DirectMessage.objects.filter(
            receiver=user,
            is_read=False,
        ).values('sender').annotate(total=Count('id'))
    }

    # Une conversation par interlocuteur
    convo_map = {}
    for msg in all_msgs:
        other = msg.receiver if msg.sender_id == user.id else msg.sender
        previous = convo_map.get(other.id)

        if previous is None or msg.created_at > previous['last_message'].created_at:
            convo_map[other.id] = {
                'user': other,
                'last_message': msg,
            }

    conversations = sorted(
        [
            {
                'user': data['user'],
                'last_message': data['last_message'],
                'unread_count': unread_counts.get(data['user'].id, 0),
            }
            for data in convo_map.values()
        ],
        key=lambda d: d['last_message'].created_at,
        reverse=True,
    )

    if active_user is not None:
        thread_messages = DirectMessage.objects.filter(
            Q(sender=user, receiver=active_user)
            | Q(sender=active_user, receiver=user)
        ).order_by('created_at')

        if request.method == 'POST':
            dm_form = DirectMessageForm(request.POST)
            if dm_form.is_valid():
                DirectMessage.objects.create(
                    sender=user,
                    receiver=active_user,
                    content=dm_form.cleaned_data['content'],
                )
                return redirect('users:messages_with', username=active_user.username)
        else:
            dm_form = DirectMessageForm()

    context = {
        'conversations': conversations,
        'active_user': active_user,
        'thread_messages': thread_messages,
        'dm_form': dm_form,
        'contact_users': contact_users,
        'contact_query': contact_query,
    }
    return render(request, 'users/messages.html', context)


@login_required
def follow_user(request, username):
    """
    Suivre un autre utilisateur.
    """
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow != request.user:
        Follow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow,
        )
    return redirect('users:user_profile', username=username)


@login_required
def unfollow_user(request, username):
    """
    Se desabonner d'un utilisateur.
    """
    user_to_unfollow = get_object_or_404(User, username=username)

    Follow.objects.filter(
        follower=request.user,
        followed=user_to_unfollow,
    ).delete()

    return redirect('users:user_profile', username=username)
