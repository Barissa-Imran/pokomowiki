from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from dictionary.models import Term


class IndexView(TemplateView):
    template_name = 'dictionary/index.html'


class AboutView(TemplateView):
    template_name = 'dictionary/about.html'


class TosView(TemplateView):
    template_name = 'dictionary/tos.html'


def define(request, term):
    word = Term.objects.get(word=term)
    context = {
        'term': word,
    }
    return render(request, "dictionary/define.html", context)
