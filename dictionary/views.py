from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView

from dictionary.models import Term
from random import choice


class IndexView(TemplateView):
    template_name = 'dictionary/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        terms = Term.objects.all()[:10]

        context.update({
            'terms': terms,
        })

        return context


class AboutView(TemplateView):
    template_name = 'dictionary/about.html'


class TosView(TemplateView):
    template_name = 'dictionary/tos.html'


def define(request, term):
    if term == "random":
        pks = Term.objects.values_list('pk', flat=True)
        random_pk = choice(pks)
        word = Term.objects.get(pk=random_pk)
    else:
        word = Term.objects.get(word=term)

    context = {
        'term': word,
    }
    return render(request, "dictionary/define.html", context)


class TermCreateView(CreateView):
    """This class allows a user to define a new word"""
    model = Term
    fields = [
        "language",
        "word",
        "defination",
        "example",
        "other_definations"
    ]

    def form_valid(self, form):
        try:
            author = self.request.user
        except:
            pass
        return super().form_valid(form)


class TermUpdateView(UpdateView):
    """ view to update word definitions"""
    model = Term
    fields = [
        "language",
        "word",
        "defination",
        "example",
        "other_definations"
    ]

    def form_valid(self, form):
        try:
            author = self.request.user
        except:
            pass
        return super().form_valid(form)

class TermDeleteView(DeleteView):
    model = Term