from django import forms
from .models import Post, Comment


class MyPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'thread', 'content', 'type', 'image']
        widgets = {
            'type': forms.Select(attrs={"class": "form-control"}),
            'thread': forms.Select(attrs={"class": "form-control"})
        }


class MyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
