# Generated by Django 4.2.6 on 2023-11-08 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media_file', '0015_sharepost_share_comment_sharepost_share_reaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFriends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cancel_request', models.ManyToManyField(null=True, related_name='cancel_request_friend', to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(null=True, related_name='friends_user', to=settings.AUTH_USER_MODEL)),
                ('requested_by', models.ManyToManyField(null=True, related_name='requested_friend', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_friend', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]