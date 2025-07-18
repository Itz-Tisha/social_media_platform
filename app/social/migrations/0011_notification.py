# Generated by Django 5.1.4 on 2025-05-24 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_delete_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=50)),
                ('webuser1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mainuser', to='social.webuser')),
                ('webuser2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inverseuser', to='social.webuser')),
            ],
        ),
    ]
