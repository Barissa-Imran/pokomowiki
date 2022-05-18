from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView, DetailView
from dictionary.models import Term, Flag
from dictionary.forms import TermForm
from random import choice
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from random import choice
from allauth.account.forms import LoginForm
import json
from django.http import JsonResponse
from django.db.models import Q, Count


class IndexView(TemplateView):
    """Handle functionality for the homepage"""
    template_name = 'dictionary/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        form = LoginForm()

        # count votes and add them to terms context--
        terms = Term.objects.all().annotate(
            upvotes_count=Count('upvote', distinct=True,
                                filter=Q(approved=True)),
            downvotes_count=Count(
                'downvote', distinct=True, filter=Q(approved=True))
        )[:10]

        context.update({
            'terms': terms,
            'form': form,
        })

        return context

    def post(self, request, *args, **kwargs):
        # check if user is authenticated
        if request.user.is_authenticated:
            # is_ajax() method deprecated in this version of django hence wrote my own
            def is_ajax(request):
                return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

            if is_ajax(request=request):
                if request.POST.get('form') == "vote":
                    term_id = request.POST.get('term_id')
                    term = get_object_or_404(Term, pk=int(term_id))
                    vote_type = request.POST.get('button')

                    userUpVotes = term.upvote.filter(
                        id=request.user.id).count()
                    userDownVotes = term.downvote.filter(
                        id=request.user.id).count()

                    if vote_type == "upVote":
                        if userUpVotes == 0 and userDownVotes == 0:
                            term.upvote.add(request.user)
                        elif userUpVotes == 1:
                            term.upvote.remove(request.user)
                        elif userDownVotes == 1 and userUpVotes == 0:
                            term.downvote.remove(request.user)
                            term.upvote.add(request.user)

                    elif vote_type == "downVote":
                        if userDownVotes == 0 and userUpVotes == 0:
                            term.downvote.add(request.user)
                        elif userDownVotes == 1:
                            term.downvote.remove(request.user)
                        elif userUpVotes == 1 and userDownVotes == 0:
                            term.upvote.remove(request.user)
                            term.downvote.add(request.user)
                elif request.POST.get('form') == "flag":
                    term_id = request.POST.get('term_id')
                    reason = request.POST.get('reason')
                    other_reason = request.POST.get('other_reason')
                    user = request.user
                    term = get_object_or_404(Term, pk=int(term_id))
                    flags = term.flag_set.all()

                    # check if flags exist
                    if flags:
                        # check if user has flags
                        flag = term.flag_set.filter(flagged_by=user)
                        if flag:
                            flag.update(reason=reason,
                                        other_reason=other_reason)
                        else:
                            flag = Flag(word=term, reason=reason,
                                        other_reason=other_reason, flagged_by=user)
                            flag.save()
                    else:
                        flag = Flag(word=term, reason=reason,
                                    other_reason=other_reason, flagged_by=user)
                        flag.save()
            else:
                pass

            # count number of votes to be shown to user after successfull post
            num_upvotes = Term.objects.all().annotate(
                upvotes_count=Count('upvote')
            )
            num_downvotes = Term.objects.all().annotate(
                downvotes_count=Count('downvote')
            )

            # convert data to json to be sent to jquery(client)
            data = json.dumps({
                'num_upvotes': num_upvotes[0].upvotes_count,
                'num_downvotes': num_downvotes[0].downvotes_count,
                'message': "Report submitted successfully"
            })

            return JsonResponse({"data": data}, status=200)
        else:
            pass

    def get(self, request, *args, **kwargs):
        # is_ajax() method deprecated in this version of django hence wrote my own
        def is_ajax(request):
            return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        
        # check if cookies are working on browser
        request.session.set_test_cookie()

        # Check that the test cookie worked
        if request.session.test_cookie_worked():
            # delete the test cookie
            request.session.delete_test_cookie()

            request.session['has_voted'] = False
       
            if is_ajax(request=request):
                
                term_id = request.GET.get('term_id')
                button = request.GET.get('button')

                request.session['term_id'] = term_id
                request.session['button'] = button
                request.session['has_voted'] = True
                
            else:
                pass
        else:
            return HttpResponse("Our site uses cookies. Please enable cookies and try again.")
        
        return super().get(request, *args, **kwargs)
class RandomView(TemplateView):
    template_name = 'dictionary/random.html'

    def get_context_data(self, **kwargs):
        context = super(RandomView, self).get_context_data(**kwargs)

        pks = Term.objects.values_list('pk', flat=True)
        random_pk = choice(pks)
        random_term = Term.objects.get(pk=random_pk)
        term = random_term

        context.update({
            'term': term,
        })

        return context

    def post(RandomView, request, *args, **kwargs):
        # reference the post method from random view
        return IndexView.post(RandomView, request, *args, **kwargs)


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


class BrowseView(TemplateView):
    """Show Terms starting with a particular character"""
    template_name = 'dictionary/browse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        char = self.kwargs['char']
        terms = Term.objects.filter(word__startswith=char).annotate(
            upvotes_count=Count('upvote', distinct=True),
            downvotes_count=Count(
                'downvote', distinct=True, filter=Q(approved=True))
        )

        context["terms"] = terms 
        context['char'] = char
        return context
    
    def post(BrowseView, request, *args, **kwargs):
        # reference the post method from random view
        return IndexView.post(BrowseView, request, *args, **kwargs)

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

    def post(TermDetailView, request, *args, **kwargs):
        # reference the post method from random view
        return IndexView.post(TermDetailView, request, *args, **kwargs)


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
