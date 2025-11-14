from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Titre de la publication',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Exprime-toi ici...',
                'rows': 3,
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-select shadow-sm type-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control shadow-sm'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ajouter un commentaire...',
            }),
        }
