from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from dictionary.models import Term
from django.shortcuts import get_object_or_404
from django.contrib import messages


@receiver(user_logged_in, dispatch_uid="vote save")
def user_logged_in(request, user, **kwargs):
    # create a vote if the user had voted while anonymous
    if request.session.get('has_voted', True):
        try:
            term_id = request.session['term_id']
            vote_type = request.session['button']
            term = get_object_or_404(Term, pk=int(term_id))

            userUpVotes = term.upvote.filter(id=request.user.id).count()
            userDownVotes = term.downvote.filter(id=request.user.id).count()

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
            try:
                del request.session['termid']
                del request.session['button']
                request.session['has_voted'] = False
            except KeyError:
                pass
        except KeyError:
            pass
    elif request.session.get('submit', True):
        try:
            request.session['language']
            try:
                # get data from session cookie
                language = request.session['language']
                clan = request.session['clan']
                word = request.session['word']
                definition = request.session['definition']
                example = request.session['example']
                other_definitions = request.session['other_definitions']

                # create term and store
                new = Term(language=language, clan=clan, word=word, definition=definition,
                    example=example, other_definitions=other_definitions, author=request.user)
                new.save()
                request.session['term_url'] = new.get_absolute_url()
                messages.add_message(request, messages.INFO,
                                    'Word added successfully, await approval. View your word on outline tab in Profile page')
                try:
                    del request.session['language']
                    del request.session['clan']
                    del request.session['word']
                    del request.session['definition']
                    del request.session['example']
                    del request.session['other_definitions']
                    request.session['submit'] = False
                except KeyError:
                    pass
            except KeyError:
                pass
        except KeyError:
            messages.add_message(request, messages.ERROR,
                                 'Word data lost during login. Please try again!')
    else:
        pass
