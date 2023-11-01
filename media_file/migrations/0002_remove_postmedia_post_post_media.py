# Generated by Django 4.2.6 on 2023-11-01 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_file', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postmedia',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.ManyToManyField(related_name='posts', to='media_file.postmedia'),
        ),
    ]