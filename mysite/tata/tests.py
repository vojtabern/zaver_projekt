from django import forms
from .models import Questions, Test

ANS = (
    ("-2", "Ne"),
    ("-1", "Spíše ne"),
    ("0", "nevím"),
    ("1", "Spíše ano"),
    ("2", "Ano"),
)


class Ans(forms.Form):

    answer = forms.ChoiceField(choices=ANS)


    # class Meta:
    #     fields = ('question', 'answer')
    #
    #     widgets = {
    #         'question': forms.TextInput(attrs={'id': 'otazka'}),
    #         'answer': forms.TextInput(attrs={'name': 'odpoved'})
    #     }

# Create your tests here.
