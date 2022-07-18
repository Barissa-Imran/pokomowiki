from django.contrib import admin
from wiki.models import Article

class ArticleAdmin(admin.ModelAdmin):
    """Article model admin config"""
    # form = ArticleAdminForm

    list_display = ('title', 'tags', 'author', 'created_at', 'updated_at',)
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['title', 'post', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at')

    #sets up slug to be generated from article name
    prepopulated_fields = {'slug': ('title',)}

#Registers article model with admin site
admin.site.register(Article, ArticleAdmin)
