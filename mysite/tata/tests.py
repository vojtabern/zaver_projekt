from django import forms

ANS = (
    ("1", "Ne"),
    ("2", "Spíše ne"),
    ("0", "nevím"),
    ("4", "Spíše ano"),
    ("5", "Ano"),
)


class Ans(forms.Form):
    answer = forms.ChoiceField(choices=ANS)
# Create your tests here.
