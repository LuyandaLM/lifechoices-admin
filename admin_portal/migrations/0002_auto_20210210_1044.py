# Generated by Django 3.1.5 on 2021-02-10 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='profile_pictures/default.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
