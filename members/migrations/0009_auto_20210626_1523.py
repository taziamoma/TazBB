# Generated by Django 3.1.7 on 2021-06-26 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20210626_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='static/avatars/default.png', upload_to='static/avatars'),
        ),
    ]
