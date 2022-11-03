from django import forms
from django import forms

from news.models import Comment, Reply

class CommentForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "id": "name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "id": "email"}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={"class": "form-control", "id": "website"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "cols": "30", "rows": "7", "id": "message"}))

    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'message']

class ReplyForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "id": "name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "id": "email"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "cols": "30", "rows": "7", "id": "message"}))

    class Meta:
        model = Reply
        fields = ['name', 'email', 'message']
        