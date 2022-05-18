from django.urls import path, re_path
from dictionary import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('random', views.RandomView.as_view(), name='random'),
    re_path(r'^browse/(?:(?P<char>.+))$', views.BrowseView.as_view(), name='browse'),
    path('about', views.AboutView.as_view(), name='about'),
    path('tos', views.TosView.as_view(), name='tos'),
    path('privacy', views.PrivacyView.as_view(), name='privacy'),
    path('dmca', views.DmcaView.as_view(), name='dmca'),
    path('content-guidelines', views.ContentGuidelinesView.as_view(), name='content_guidelines'),
    path('editor', views.EditorView.as_view(), name='editor'),

    re_path('term/(?P<pk>[^/]+)\\Z', views.TermDetailView.as_view(), name='term_detail'),
    path('add', views.TermCreateView.as_view(), name='add'),
    re_path('term/(?P<pk>[^/]+)/update',
         views.TermUpdateView.as_view(), name='term_update'),
    re_path('term/(?P<pk>[^/]+)/delete',
         views.TermDeleteView.as_view(), name='term_delete')
]

# (?P<id>\w+)/$
# 'term/(?P<pk>[^/]+)\\Z'
