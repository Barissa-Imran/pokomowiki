from django import forms
from dictionary.models import Term, Flag


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['word', 'definition', 'example', 'example_translation',
                  'other_definitions', 'language', 'dialect']

class TermAdminForm(forms.ModelForm):
    """Admin interface term form"""
    class Meta:
        model = Term
        fields = ['word', 'definition', 'example', 'example_translation',
                  'other_definitions', 'language', 'dialect', 'meta_keywords', 'meta_description']

    # creates meta keywords and decription on save
    def save(self, commit=True):
        keywords = []

        word = self.cleaned_data['word'].split(" ")
        keywords += word

        definition = self.cleaned_data['definition'].split(" ")
        keywords += definition

        if self.cleaned_data['other_definitions']:
            other_definitions = self.cleaned_data['other_definitions'].split(
                " ")
            keywords += other_definitions
        else:
            pass

        str_keywords = ', '.join([str(word) for word in keywords])

        self.cleaned_data['meta_keywords'] = str_keywords
        self.cleaned_data['meta_description'] = self.cleaned_data['definition']
        return super(TermAdminForm, self).save(commit=commit)
