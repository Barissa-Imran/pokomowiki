from pyexpat import model
from django import forms
from dictionary.models import Term, Flag


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['word', 'definition', 'example',
                  'other_definitions', 'language', 'clan']
