# Generated by Django 5.2 on 2025-06-19 08:25

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='banner_image',
            field=models.ImageField(blank=True, default='/club_banners/default.jpg', null=True, upload_to='club_banners/'),
        ),
        migrations.AlterField(
            model_name='club',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True),
        ),
    ]
