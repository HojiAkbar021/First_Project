# Generated by Django 4.0.5 on 2022-07-03 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_rename_discribtion_post_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='currency',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]