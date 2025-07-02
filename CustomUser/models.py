from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    phonenumber = PhoneNumberField("Номер телефона", null=False, blank=False, unique=True)
    avatar = models.ImageField("картинка", upload_to="avatars/", null=True, blank=True)
    name = models.CharField("Имя", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        indexes = [
            models.Index(fields=["phonenumber"]),
        ]

    def __str__(self):
        return f"{self.name} {self.phonenumber}"
