# Generated by Django 5.0.8 on 2024-08-22 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_ad_latitude_ad_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='address',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]