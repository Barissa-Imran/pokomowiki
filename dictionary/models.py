from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

user = get_user_model()

languages = [
    ( "Upper Pokomo", "Upper Pokomo"),
    ("Malanchini", "Malanchini")
]


class Term(models.Model):
    """Store added words in the dictionary"""
    language = models.CharField(choices=languages, max_length=50)
    word = models.CharField(null=False, max_length=150)
    defination = models.TextField(null=False)
    example = models.TextField()
    other_definations = models.TextField(null=True, blank=True)
    user = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    # date
    # upvote
    # downvote
    # flag

    def __str__(self):
        return self.word

    # def get_absolute_url(self):
    #     return reverse("term_detail", kwargs={
    #         "word": self.word
    #     })
