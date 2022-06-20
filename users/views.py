from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Profile
from dictionary.models import Flag, Term
from django.contrib.auth import get_user_model
from django.db.models import Count, F
import json
from django.http import JsonResponse
from users.models import Profile
from django.contrib import messages

User = get_user_model()


class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=user_pk)
        profile = get_object_or_404(Profile, user=user)
        flags = Flag.objects.filter(flagged_by=user)
        term_count = Term.objects.filter(author=user)
        upvotes = Term.objects.filter(
            upvote__in=[self.request.user.id]).count()
        downvotes = Term.objects.filter(
            downvote__in=[self.request.user.id]).count()

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
        terms = Term.objects.filter(author=user).annotate(upvotes_count=Count(
            'upvote', distinct=True), downvotes_count=Count('downvote', distinct=True))[:10]
        my_flags = Flag.objects.filter(flagged_by=user)
        flags = Flag.objects.filter(word__author=user)
        usergroup = None
        usergroup = user.groups.values_list('name', flat=True).first()
        profile = get_object_or_404(Profile, user=user)

        print(profile)

        context.update({
            'terms': terms,
            'my_flags': my_flags,
            'flags': flags,
            'usergroup': usergroup,
            'profile': profile
        })

        return context


class ReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'users/review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        terms = Term.objects.filter(approved=False)
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        context.update({
            'terms': terms,
            'profile': profile
        })
        return context

    def post(self, request, *args, **kwargs):
        message = None
        if request.POST.get('type') == "approve":
            termId = request.POST.get('termId')
            term = Term.objects.get(pk=termId)
            editor = request.user

            # approve term & add reputation points
            try:

                Profile.objects.filter(user=editor).update(
                    reputation=F('reputation') + 5)  # add 5 points to editor
                Profile.objects.filter(user=term.author).update(
                    reputation=F('reputation') + 15)  # add 15 points to author

                term.approved = True
                term.save()

                message = "Term approved successfully"
            except:
                message = "Term Approval failed. Please try again Later!"
                data = json.dumps({
                    'message': message
                })
                return JsonResponse({"data": data}, status=500)
        else:
            pass
        data = json.dumps({
            'message': message
        })
        return JsonResponse({"data": data}, status=200)


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        context.update({
            'profile': profile
        })
        return context

    def post(self, request, *args, **kwargs):
        def is_ajax(request):
            return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        message = None
        if is_ajax(request=request):
            user = request.user
            username = request.POST.get("username")
            if user.username == username:
                user.is_active = False
                user.save()
                msg = 'Profile disabled successfully'
                data = json.dumps({
                    'msg': msg,
                })
                return JsonResponse({'data': data}, status=200)
            else:
                msg = "Username mismatch. Please try again!"
                data = json.dumps({
                    'msg': msg,
                })
                return JsonResponse({'data': data}, status=404)
        else:
            pass
        return render(request, "users/settings.html", {'message': message})
