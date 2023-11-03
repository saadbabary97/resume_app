# Generated by Django 4.2.6 on 2023-11-03 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_file', '0011_postreaction_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postreaction',
            name='reaction_type',
            field=models.CharField(choices=[('like', 'Like'), ('dislike', 'Dislike'), ('love', 'Love'), ('haha,', 'Haha,'), ('wow,', 'Wow,'), ('angry,', 'Angry,'), ('sad,', 'Sad,')], max_length=20),
        ),
    ]
