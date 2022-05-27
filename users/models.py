from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default='default.png', upload_to='profile_images')
    bio = models.TextField()
    reputation = models.IntegerField(blank=True)

    def __str__(self):
        return self.user.username


