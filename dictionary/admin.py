from django.contrib import admin
from .models import Term, Flag
from dictionary.forms import TermAdminForm


class TermAdmin(admin.ModelAdmin):
    """Term model admin config"""
    form = TermAdminForm

    list_display = ('word', 'language', 'dialect', 'date', 'approved')
    list_display_links = ('word',)
    list_per_page = 50
    ordering = ['-date']
    search_fields = ['word', 'dialect', 'definition',
                     'other_definitions', 'meta_keywords', 'meta_description']
    exclude = ('date',)

    # sets up keywords and description from term definition
    prepopulated_fields = {
        'meta_description': ('definition', 'other_definitions')
    }


admin.site.register(Term, TermAdmin)
admin.site.register(Flag)
