# Generated by Django 4.1 on 2022-08-22 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='blank_profile', upload_to='profile_images'),
        ),
    ]