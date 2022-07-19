from django.db import models
from apps.users.models import User
from apps.categories.models import Category
from django.db.models.signals import pre_save
from apps.posts.slug_generator import unique_slug_generators

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="post_category", blank=True, null=True)
    price = models.PositiveIntegerField()
    post_image = models.ImageField(upload_to = "post_image/")
    created = models.DateTimeField(auto_now_add=True)
    CHOICE_CURRENCY = (
        ('KGZ', 'KGZ'),
        ('USD', 'USD'),
        ('EURO', 'EURO'),
        ('RUB', 'RUB'),
        ('Договорная', 'Договорная'),
    )
    currency = models.CharField(choices=CHOICE_CURRENCY, default='Договорная', max_length=100)
    valid = models.BooleanField(default=True)
    STATUS_POST = (
        ('Free', 'Free'),
        ('Pro', 'Pro'),
    )
    status = models.CharField(choices=STATUS_POST, max_length=10, default='Free')
    slug = models.SlugField(blank=True, null = True, unique = True, verbose_name="Человекопонятный URL (само генерация)")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Обявление"
        verbose_name_plural = "Обявления"

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="image_post")
    image = models.ImageField(upload_to = "second_post_image/")

    class Meta:
        verbose_name = "Дополнительная фотография"
        verbose_name_plural = "Дополнительные фотографии"

class FavoritePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="favorite_post")

    def __str__(self):
        return f"{self.user.username} {self.post.title}"

    class Meta:
        verbose_name = "Понравилось пост"
        verbose_name_plural = "Понравились посты"

def slag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generators(instance)


pre_save.connect(slag_pre_save_receiver, sender=Post)       