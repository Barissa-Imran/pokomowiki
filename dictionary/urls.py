from django.urls import path, re_path
from dictionary import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about', views.AboutView.as_view(), name='about'),
    path('tos', views.TosView.as_view(), name='tos'),
    re_path(r'^define/term=(?P<term>\w+)$', views.define, name='define'),
    path('add', views.TermCreateView.as_view(), name='add'),
    path('term/<word>/update', views.TermUpdateView.as_view(), name='term_update'),
    path('term/<word>/delete', views.TermDeleteView.as_view(), name='term_delete')
]
