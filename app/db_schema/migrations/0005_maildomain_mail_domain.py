# Generated by Django 4.0.10 on 2024-03-23 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_mailbox', '0008_auto_20190219_1553'),
        ('db_schema', '0004_mail_processed'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailDomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(blank=True, max_length=255, null=True)),
                ('port', models.IntegerField(blank=True, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('box', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_mailbox.mailbox')),
            ],
            options={
                'verbose_name': 'メールドメイン',
                'verbose_name_plural': 'メールドメイン管理',
            },
        ),
        migrations.AddField(
            model_name='mail',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db_schema.maildomain'),
        ),
    ]
