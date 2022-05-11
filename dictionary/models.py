from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

languages = [
    ("Upper Pokomo", "Upper Pokomo"),
    ("Malanchini", "Malanchini")
]

clans = [
    ("Ndera", "Ndera"),
    ("Zubaki", "Zubaki"),
    ("Kinakomba", "Kinakomba"),
    ("Gwano", "Gwano"),
    ("Malanchini", "Malanchini"),
    ("None", "None")
]

reasons = [
    ("wrong definition", "wrong definition"),
    ("hate speech", "hate speech"),
    ("other", "other")
]


class Term(models.Model):
    """Store added words in the dictionary"""
    language = models.CharField(choices=languages, max_length=50)
    clan = models.CharField(choices=clans, max_length=50)
    word = models.CharField(null=False, max_length=150, unique=True)
    definition = models.TextField(null=False)
    example = models.TextField()
    other_definitions = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now=True)
    upvote = models.IntegerField(default=0, null=True, blank=True)
    downvote = models.IntegerField(default=0, null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.word

    def get_absolute_url(self):
        return reverse("term_detail", kwargs={
            "pk": self.pk
        })


class Flag(models.Model):
    """handle flags made to words by users"""
    word = models.ForeignKey(Term, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, choices=reasons)
    other_reason = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    flagged_by = models.ForeignKey(
        User, related_name="created_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.word
