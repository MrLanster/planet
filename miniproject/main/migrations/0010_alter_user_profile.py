# Generated by Django 4.2.6 on 2024-03-30 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.CharField(default='none.png', max_length=100),
        ),
    ]
