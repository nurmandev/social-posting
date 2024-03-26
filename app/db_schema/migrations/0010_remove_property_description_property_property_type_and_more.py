# Generated by Django 4.0.10 on 2024-03-26 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_schema', '0009_imap'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='description',
        ),
        migrations.AddField(
            model_name='property',
            name='property_type',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='status',
            name='status_type',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], max_length=50, null=True),
        ),
    ]