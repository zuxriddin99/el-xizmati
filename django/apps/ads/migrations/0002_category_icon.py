# Generated by Django 5.0.6 on 2024-08-12 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.FileField(null=True, upload_to='categories/'),
        ),
    ]
