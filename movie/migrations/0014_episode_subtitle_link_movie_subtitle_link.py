# Generated by Django 5.1.4 on 2025-01-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0013_downloadfile_10_bit_variant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='subtitle_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='subtitle_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]