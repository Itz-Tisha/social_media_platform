# Generated by Django 5.1.4 on 2025-05-23 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_rename_phone_webuser_password'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='post',
            new_name='web_post',
        ),
    ]
