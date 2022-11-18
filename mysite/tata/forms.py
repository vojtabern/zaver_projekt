from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label='Email')
    subject = forms.CharField(required=True, label='Předmět')
    message = forms.CharField(widget=forms.Textarea, required=True, label='Zpráva')