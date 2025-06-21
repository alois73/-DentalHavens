from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email'})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'id_message', 'rows': '5'})
    )
