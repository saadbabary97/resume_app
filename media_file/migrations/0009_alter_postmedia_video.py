# Generated by Django 4.2.6 on 2023-11-01 17:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_file', '0008_alter_postmedia_image_alter_postmedia_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmedia',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='media/videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mov', 'avi', 'mp4', 'webm', 'mkv'])]),
        ),
    ]
