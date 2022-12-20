from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label='Email')
    subject = forms.CharField(required=True, label='Předmět')
    message = forms.CharField(widget=forms.Textarea, required=True, label='Zpráva')
    captcha = CaptchaField()


class User_Id(forms.Form):
    user = forms.EmailField(required=True, label='Email')