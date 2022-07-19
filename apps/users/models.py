from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from apps.posts.slug_generator import unique_slug_generators

class User(AbstractUser):
    profile_image = models.ImageField(upload_to = 'profile_image/')
    phone = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null = True, unique = True, verbose_name="Человекопонятный URL (само генерация)")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

def slag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generators(instance)


pre_save.connect(slag_pre_save_receiver, sender=User)