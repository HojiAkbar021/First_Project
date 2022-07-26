# Generated by Django 4.0.6 on 2022-07-14 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_postimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Человекопонятный URL (само генерация)'),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('Free', 'Free'), ('Pro', 'Pro')], default='Free', max_length=10),
        ),
    ]
