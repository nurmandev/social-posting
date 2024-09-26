# Generated by Django 5.1.1 on 2024-09-13 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0004_userinfo_is_facebook_userinfo_is_instagram_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='is_facebook',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='is_tiktok',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='is_instagram',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='is_youtube',
            field=models.BooleanField(default=False),
        ),
    ]