from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from dictionary.models import dialects

User = get_user_model()


class Article(models.Model):
    """Create articles for the wiki app"""
    # Individual status
    SUBMITTED = 1
    EDITTED = 2
    PUBLISHED = 3
    REJECTED = 4

    # Article statuses
    ARTICLE_STATUSES = (
        (SUBMITTED, 'Submitted'),
        (EDITTED, 'Editted'),
        (PUBLISHED, 'Published'),
        (REJECTED, 'Rejected')
    )

    # Article info
    title = models.CharField(max_length=255, unique=True)
    post = models.TextField(null=False)
    tags = models.CharField(choices=dialects, max_length=50)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=ARTICLE_STATUSES, default=SUBMITTED)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text="Unique value for article page URL, created from title.")
    meta_keywords = models.CharField("Meta Keywords", max_length=255,
                                     help_text="Comma-delimited set of SEO keywords for meta tag")
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')
    upvote = models.ManyToManyField(
        User, blank=True, related_name='articleUpVotes')
    downvote = models.ManyToManyField(
        User, blank=True, related_name='articleDownVotes')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"article_slug": self.slug})
    
    # @property
    # def get_meta_keywords(self):
    #     pass