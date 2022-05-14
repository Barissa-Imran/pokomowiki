from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView, DetailView
from dictionary.models import Term
from dictionary.forms import TermForm
from random import choice
from django.contrib import messages
from django.shortcuts import reverse
from random import choice
from allauth.account.forms import LoginForm


class IndexView(TemplateView):
    template_name = 'dictionary/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        terms = Term.objects.filter(approved=True)[:10]
        form = LoginForm()

        context.update({
            'terms': terms,
            'form': form
        })

        return context
    
    def post(self, request, *args, **kwargs):
        # is ajax method deprecated in this version of django hence wrote my own
        def is_ajax(request):
            print(request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest')
            return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        if is_ajax(request=request):
            if request.POST.get('button') == "upVote":
                term_id = request.POST.get('term_id')
                term = Term.objects.get(id=int(term_id))
                term.upvote += 1
                term.save()
            elif request.POST.get('button') == "downVote":
                term_id = request.POST.get('term_id')
                term = Term.objects.get(id=int(term_id))
                term.downvote -= 1
                term.save()
        else:
            pass
        
        context = self.get_context_data()
        return render(request, "dictionary/index.html", context)


class RandomView(TemplateView):
    template_name = 'dictionary/random.html'

    def get_context_data(self, **kwargs):
        context = super(RandomView, self).get_context_data(**kwargs)

        pks = Term.objects.values_list('pk', flat=True)
        random_pk = choice(pks)
        random_term = Term.objects.get(pk=random_pk)
        
        context.update({
            'term': random_term,
        })

        return context

class AboutView(TemplateView):
    template_name = 'dictionary/about.html'


class TosView(TemplateView):
    template_name = 'dictionary/tos.html'

class PrivacyView(TemplateView):
    template_name = 'dictionary/privacy.html'

class DmcaView(TemplateView):
    template_name = 'dictionary/dmca.html'

class ContentGuidelinesView(TemplateView):
    template_name = 'dictionary/content_guidelines.html'

class EditorView(TemplateView):
    template_name = 'dictionary/editor.html'


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

    # def get_success_url(self):
    #     term = self.object.id
    #     return reverse("define", args=(term,))

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
        except:
            pass
        return super().form_valid(form)

class TermDetailView(DetailView):
    model = Term


class TermUpdateView(UpdateView):
    """ view to update word definitions"""
    model = Term
    # template_name = 'dictionary/term_form.html'
    form_class = TermForm

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
        except:
            pass
        return super().form_valid(form)


class TermDeleteView(DeleteView):
    model = Term
    success_url = "dictionary/index.html"
    
