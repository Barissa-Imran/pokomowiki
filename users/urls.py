from django.urls import path
from users import views
urlpatterns = [
    path("profile/<int:pk>/<str:username>", views.ProfileView.as_view(), name='profile'),
    path("review",views.ReviewView.as_view(), name='review'),
    path("outline", views.OutlineView.as_view(), name='outline'),
    path("settings", views.SettingsView.as_view(), name='settings')
]
