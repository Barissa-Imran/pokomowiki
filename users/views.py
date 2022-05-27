from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Profile
from dictionary.models import Flag
from django.contrib.auth import get_user_model

User = get_user_model()
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=user_pk)
        profile = get_object_or_404(Profile, user=user)
        flags = get_object_or_404(Flag, flagged_by=user)
        flag = Flag.objects.all()
        print(flag.count())

        context.update({
            'profile': profile,
            'user': self.request.user,
            'flags': flags
        })

        return context

class ReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'users/words.html'

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/settings.html'
