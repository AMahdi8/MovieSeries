# Generated by Django 5.1.4 on 2024-12-22 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_rename_release_date_movie_release_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='Languages',
            field=models.ManyToManyField(blank=True, related_name='movies', to='movie.language'),
        ),
    ]