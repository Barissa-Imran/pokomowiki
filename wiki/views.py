from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from wiki.models import Article
from django.urls import reverse
from wiki.forms import ArticleForm


class WikiView(TemplateView):
    template_name = 'wiki/wiki.html'


class ArticleCreateView(CreateView):
    """Create article in wiki app"""
    model = Article
    form_class = ArticleForm

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            messages.success(self.request, "Article published successfully")
        except:
            messages.error(
                self.request, "Article publishing failed, please try again later")
        return super().form_valid(form)


class ArticleUpdateView( LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update article in wiki app"""
    model = Article
    form_class = ArticleForm

    def test_func(self):
        user = self.request.user
        article = self.get_object()
        usergroup = None
        usergroup = self.request.user.groups.values_list('name', flat=True).first()
        if usergroup == 'Editor' or Article.author == user:
            return True
        return False


    # def form_valid(self, form):
    #     return super().form_valid(form)

class ArticleDetailView(DetailView):
    model = Article
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             'Word deleted successfully')
        return reverse('wiki')

    def test_func(self):
        user = self.request.user
        term = self.get_object()
        if user.is_staff or term.author == user:
            return True
        return False
