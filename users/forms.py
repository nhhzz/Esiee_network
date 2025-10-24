from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

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
    class Meta:
        model = User
        fields = ('username','email')
    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if not email.endswith(ESIEE_DOMAIN):
            raise forms.ValidationError("L'email doit se terminer par @edu.esiee.fr")
        qs = User.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Cette adresse est déjà utilisée.")
        return email
