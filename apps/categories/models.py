from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    discribtion = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категорие"
        verbose_name_plural = "Категория"