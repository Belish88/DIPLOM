# Generated by Django 5.0.1 on 2024-01-31 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='invite_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]