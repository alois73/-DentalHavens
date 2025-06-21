from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    custom_request = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Describe your dental needs, e.g. veneers, implants, whitening...'
        }),
        required=False,
        label="Describe your dental request"
    )

    class Meta:
        model = Client
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'tour_option', 
            'custom_request',
        ]
