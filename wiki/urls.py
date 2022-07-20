from django.urls import path
from wiki import views

urlpatterns = [
    path("", views.WikiView.as_view(), name='wiki'),
    path("article/new", views.ArticleCreateView.as_view(), name="new_article"),
    path("article/<slug:slug>", views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<slug:slug>/delete', views.ArticleDeleteView.as_view(), name='article_delete')
]