# Generated by Django 5.2 on 2025-06-22 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webusers', '0008_alter_userprofile_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='roll_number',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
