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

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user", verbose_name="От пользователя")
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_for_user", verbose_name="К пользователю")
    rating = models.PositiveBigIntegerField(default=0, verbose_name="Ретинг")
    title = models.TextField(max_length=100)
    text = models.TextField(verbose_name="Текст")
    created = models.DateTimeField(auto_now_add=True)
    STATUS_COMMENT = (
        ('В ожидании', 'В ожидании'),
        ('Не принята', 'Не принята'),
        ('Принята', 'Принята'),
    )
    status_comment = models.CharField(choices=STATUS_COMMENT, max_length=30, verbose_name="Статус комментария", default="В ожидании")

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = "Комментарий пользователю"
        verbose_name_plural = "Комментарии пользователям"