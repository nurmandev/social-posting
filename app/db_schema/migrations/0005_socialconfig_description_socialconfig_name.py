# Generated by Django 5.1.1 on 2024-09-08 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_schema', '0004_schedulevideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialconfig',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='socialconfig',
            name='name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]