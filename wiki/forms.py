from django import forms
from wiki.models import Article

class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ['title', 'post', 'tags']