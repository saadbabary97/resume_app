# Generated by Django 4.2.6 on 2023-10-24 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.IntegerField()),
                ('email', models.EmailField(default=None, max_length=254, null=True, unique=True)),
                ('education', models.TextField(blank=True, null=True)),
                ('work_experience', models.TextField(blank=True, null=True)),
                ('skills', models.TextField()),
                ('additional_information', models.TextField(blank=True, null=True)),
                ('hobbies', models.TextField(blank=True, null=True)),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
