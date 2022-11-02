from django import forms
from django import forms

from news.models import Comment, Reply

class CommentForm(forms.ModelForm):
    name = forms.CharField()
    email = forms.EmailField()
    website = forms.URLField(required=False)
    message = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'message']

class ReplyForm(forms.ModelForm):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Reply
        fields = ['name', 'email', 'message']
        