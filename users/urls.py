from django.urls import path
from users import views
urlpatterns = [
    path("profile", views.ProfileView.as_view(), name='profile')
]
