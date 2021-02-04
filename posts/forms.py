from django import forms

from .views import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
