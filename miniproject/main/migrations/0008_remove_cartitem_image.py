# Generated by Django 5.0.3 on 2024-03-14 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_item_cartitem_filename_remove_cartitem_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='image',
        ),
    ]
