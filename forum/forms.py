from django import forms
from .models import Post, Thread


class NewThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
        }


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_body',)

        widgets = {
            'post_body': forms.Textarea(attrs={'class': 'form-control', 'verbose_name': ''}),
        }


class QuickReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_body',)

        widgets = {
            'post_body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class SearchThreadsForm(forms.Form):
    keywords = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter keywords', 'class': 'form-control'}))
    authors = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter author', 'class': 'form-control', 'required':'false'}))
