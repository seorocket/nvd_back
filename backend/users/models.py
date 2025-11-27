from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("Имя"), max_length=150)
    last_name = models.CharField(_("Фамилия"), max_length=150)
    email = models.EmailField(_("E-mail"), max_length=254, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")



class TelegramUser(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='telegram'
    )
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    auth_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.username} - {self.telegram_id}"