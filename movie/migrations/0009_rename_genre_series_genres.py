# Generated by Django 5.1.4 on 2024-12-24 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_alter_episode_description_alter_movie_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='series',
            old_name='genre',
            new_name='genres',
        ),
    ]
