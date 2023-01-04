from django import forms
from django.forms.formsets import BaseFormSet

ANS = (
    ("-2", "Ne"),
    ("-1", "Spíše ne"),
    ("0", "nevím"),
    ("1", "Spíše ano"),
    ("2", "Ano"),
)


class Ans(forms.Form):
    answer = forms.ChoiceField(choices=ANS)

class Formset(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two items have the same full name,
        and that all items have a first and a last name.
        """
        if any(self.errors):
            return

        answers = []
        values = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                answers = form.cleaned_data['answer']
                # values = form.cleaned_data['values']

                # Check that no two items have the same combination of first and last name
                if answers and values:
                    if answer in answers:
                        if value is values[answer.index(answer)]:
                            duplicates = True
                    answers.append(answer)
                    values.append(value)


                if duplicates:
                    raise forms.ValidationError(
                        'Auditees must have unique Names.',
                        code='duplicate_auditees'
                    )





# Create your tests here.
