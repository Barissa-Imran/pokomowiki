from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView

from dictionary.models import Term
from dictionary.forms import TermForm
from random import choice
from django.contrib import messages
from django.shortcuts import reverse


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
    # elif term == "term":
    #     word = Term.objects.get(word=term)
    else:
        word = Term.objects.get(pk=term)

    context = {
        'term': word,
    }
    return render(request, "dictionary/define.html", context)


class TermCreateView(CreateView):
    """This class allows a user to define a new word"""
    model = Term
    form_class = TermForm

    def get_success_url(self):
        term = self.object.id
        return reverse("define", args=(term,))

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
        except:
            pass
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = TermForm(request.POST)
    #     if form.is_valid():
    #         try:
    #             word = form.cleaned_data.get('word')
    #             definition = form.cleaned_data.get('definition')
    #             example = form.cleaned_data.get('example')
    #             other_definition = form.cleaned_data.get('other_definition')
    #             language = form.cleaned_data.get('language')

    #             TermForm.save()
    #         except:
    #             messages.error(request, "error saving word")

    #     return render(request, "dictionary/define.html")


class TermUpdateView(UpdateView):
    """ view to update word definitions"""
    model = Term
    fields = [
        "language",
        "word",
        "definition",
        "example",
        "other_definitions"
    ]

    def form_valid(self, form):
        try:
            author = self.request.user
        except:
            pass
        return super().form_valid(form)


class TermDeleteView(DeleteView):
    model = Term
