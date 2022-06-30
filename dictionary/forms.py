from pyexpat import model
from django import forms
from dictionary.models import Term, Flag


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['word', 'definition', 'example', 'example_translation',
                  'other_definitions', 'language', 'clan']
