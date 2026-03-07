from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, DirectMessage

ESIEE_DOMAIN='@edu.esiee.fr'

class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Adresse ESIEE', help_text='Utilise ton email @edu.esiee.fr')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email')
    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if not email.endswith(ESIEE_DOMAIN):
            raise forms.ValidationError("Utilise une adresse se terminant par @edu.esiee.fr")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Cette adresse est déjà utilisée.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur")

class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        label="Changer votre nom d'utilisateur",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Entrez votre nouveau nom d'utilisateur",
            }
        ),
    )

    profile_image = forms.ImageField(
        label="Ajouter / Modifier votre photo de profil",
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "profile_image"]

class DirectMessageForm(forms.ModelForm):
    content = forms.CharField(
        label="Votre message",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Écrire un message…",
            }
        ),
    )

    class Meta:
        model = DirectMessage
        fields = ["content"]