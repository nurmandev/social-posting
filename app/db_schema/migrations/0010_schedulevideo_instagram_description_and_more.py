# Generated by Django 5.1.1 on 2024-09-14 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_schema', '0009_rename_instagram_busiess_id_socialconfig_instagram_business_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulevideo',
            name='instagram_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='schedulevideo',
            name='socials',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='schedulevideo',
            name='tiktok_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='schedulevideo',
            name='youtube_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='schedulevideo',
            name='youtube_title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
