from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Profile
from dictionary.models import Flag, Term
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=user_pk)
        profile = get_object_or_404(Profile, user=user)
        flags = Flag.objects.filter(flagged_by=user)
        term_count = Term.objects.filter(author=user)
        upvotes = Term.objects.filter(upvote__in=[self.request.user.id]).count()
        downvotes = Term.objects.filter(downvote__in=[self.request.user.id]).count()   

        votes = upvotes + downvotes       

        context.update({
            'profile': profile,
            'user': self.request.user,
            'flags': flags.count(),
            'term_count': term_count.count(),
            'votes': votes
        })

        return context

class OutlineView(LoginRequiredMixin, TemplateView):
    template_name = 'users/outline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        terms = Term.objects.filter(author=user).annotate(upvotes_count=Count('upvote', distinct=True),downvotes_count=Count('downvote', distinct=True))[:10]
        my_flags = Flag.objects.filter(flagged_by=user)
        flags = Flag.objects.filter(word__author=user)

        context.update({
            'terms': terms,
            'my_flags': my_flags,
            'flags': flags
        })

        return context

class ReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'users/review.html'

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/settings.html'
