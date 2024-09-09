# Generated by Django 5.0.8 on 2024-09-08 08:19

import apps.chat.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_count_unread_messages_chat_last_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.RemoveField(
            model_name='chat',
            name='is_tech_support',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='telegram_group_id',
        ),
        migrations.CreateModel(
            name='TechSupportChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('telegram_group_id', models.CharField(blank=True, max_length=255, null=True)),
                ('has_unread_message', models.BooleanField(default=False)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tech_support', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tech Support Chat',
                'verbose_name_plural': 'Tech Support Chats',
                'db_table': 'tech_support_chats',
            },
        ),
        migrations.CreateModel(
            name='TechSupportMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('was_read', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tech_support_messages', to=settings.AUTH_USER_MODEL)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.techsupportchat')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='chat.techsupportmessage')),
            ],
            options={
                'verbose_name': 'Tech Support Message',
                'verbose_name_plural': 'Tech Support Messages',
                'db_table': 'tech_support_messages',
            },
        ),
        migrations.CreateModel(
            name='TechSupportMessageMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=apps.chat.models.message_media_directory_path)),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default='image', max_length=6)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='chat.techsupportmessage')),
            ],
            options={
                'verbose_name': 'Message Media',
                'verbose_name_plural': 'Message Medias',
                'db_table': 'tech_support_message_medias',
            },
        ),
    ]
