# Generated by Django 3.1.7 on 2021-06-26 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_auto_20210626_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='avatars/default.png', upload_to='avatars'),
        ),
    ]
