# Generated by Django 5.0.8 on 2024-09-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_message_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='techsupportmessage',
            name='text',
            field=models.TextField(blank=True, default=''),
        ),
    ]
