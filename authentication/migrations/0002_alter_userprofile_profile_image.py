# Generated by Django 4.2.5 on 2023-09-10 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile/default.jpg', null=True, upload_to='profile'),
        ),
    ]
