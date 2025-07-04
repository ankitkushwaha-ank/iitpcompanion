# Generated by Django 5.2 on 2025-06-22 09:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webusers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(max_length=20, unique=True)),
                ('department', models.CharField(max_length=100)),
                ('year', models.IntegerField(choices=[(1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th')])),
                ('hostel', models.CharField(max_length=100)),
                ('profile_image', models.ImageField(default='profile_images/default.png', upload_to='profile_images/')),
                ('mobile_number', models.CharField(blank=True, max_length=15)),
                ('saved_foods', models.JSONField(blank=True, default=list)),
                ('saved_routes', models.JSONField(blank=True, default=list)),
                ('saved_assignments', models.JSONField(blank=True, default=list)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Webusers.users')),
            ],
        ),
    ]
