# Generated by Django 5.2 on 2025-06-28 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0005_alter_menuitem_canteen_alter_menuitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(default='menu_items/set-vector.jpg', upload_to='menu_images/'),
        ),
    ]
