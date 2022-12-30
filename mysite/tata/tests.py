from django import forms

ANS = (
    ("-2", "Ne"),
    ("-1", "Spíše ne"),
    ("0", "nevím"),
    ("1", "Spíše ano"),
    ("2", "Ano"),
)


class Ans(forms.Form):
    answer = forms.ChoiceField(choices=ANS)
# Create your tests here.
