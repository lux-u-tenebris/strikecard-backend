# Generated by Django 5.2 on 2025-06-10 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chapters', '0004_chapter_nearby_chapters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapterzip',
            name='state',
        ),
    ]
