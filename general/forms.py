from django import forms
from django import forms

from general.models import Suscriber

class SuscriberForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Your Email'}))

    class Meta:
        model = Suscriber
        fields = ['email']