# Generated by Django 5.1.1 on 2024-09-12 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='is_facebook',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='is_instagram',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='is_youtube',
            field=models.BooleanField(default=True),
        ),
    ]
