# Generated by Django 5.0.8 on 2024-09-07 19:44

import apps.chat.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_tech_support', models.BooleanField(default=False)),
                ('telegram_group_id', models.CharField(blank=True, max_length=255, null=True)),
                ('users', models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
                'db_table': 'chats',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('was_read', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_messages', to=settings.AUTH_USER_MODEL)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chat')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='chat.message')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'db_table': 'messages',
            },
        ),
        migrations.CreateModel(
            name='MessageMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=apps.chat.models.message_media_directory_path)),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default='image', max_length=6)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='chat.message')),
            ],
            options={
                'verbose_name': 'Message Media',
                'verbose_name_plural': 'Message Medias',
                'db_table': 'message_medias',
            },
        ),
    ]
