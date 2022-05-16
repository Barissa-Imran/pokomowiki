from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView, DetailView
from dictionary.models import Term, Flag
from dictionary.forms import TermForm
from random import choice
from django.contrib import messages
from django.shortcuts import get_object_or_404
from random import choice
from allauth.account.forms import LoginForm
import json
from django.http import JsonResponse
from django.db.models import Q, Count



class IndexView(TemplateView):
    template_name = 'dictionary/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        form = LoginForm()

        # term = get_object_or_404(Term, pk=int(1))
        # flag = term.flag_set.all()

        # # check if flags exist
        #     # check if user has flags
        #         # if yes then update with data
        #         # if no then create new flag
        # # if don't exist then create flag
        #     # create from received data and save
        
        # if flag:
        #     new = term.flag_set.filter(flagged_by=self.request.user)
        #     print(new[0].date)
        #     new.update(reason="Hate speech", other_reason="")
        #     print(new[0].reason)
        #     print(new[0].date)

        # else:
        #     pass
            

        terms = Term.objects.all().annotate(
            upvotes_count=Count('upvote', distinct=True, filter=Q(approved=True)), 
            downvotes_count=Count('downvote', distinct=True, filter=Q(approved=True))
        )[:10]

        context.update({
            'terms': terms,
            'form': form,
        })

        return context

    def post(self, request, *args, **kwargs):
        # check if user is authenticated
        if request.user != None:
            # is ajax method deprecated in this version of django hence wrote my own
            def is_ajax(request):
                return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

            if is_ajax(request=request):
                if request.POST.get('form') == "vote":
                    term_id = request.POST.get('term_id')
                    term = get_object_or_404(Term, pk=int(term_id))
                    vote_type = request.POST.get('button')

                    userUpVotes = term.upvote.filter(id = request.user.id).count()
                    userDownVotes = term.downvote.filter(id = request.user.id).count()

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
                        # check if user has flags
                            # if yes then update with data
                            # if no then create new flag
                    # if don't exist then create flag
                        # create from received data and save

                    if flags:
                        flag = term.flag_set.filter(flagged_by=user)
                        if flag:
                            flag.update(reason=reason, other_reason=other_reason)
                            print(reason)
                        else:
                            flag = Flag(word=term, reason=reason, other_reason=other_reason, flagged_by=user)
                            flag.save()
                    else:
                        flag = Flag(word=term, reason=reason, other_reason=other_reason, flagged_by=user)
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
