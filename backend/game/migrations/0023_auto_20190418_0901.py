# Generated by Django 2.1.4 on 2019-04-18 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0022_game_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='completed',
        ),
        migrations.AddField(
            model_name='player',
            name='completed_time',
            field=models.DateTimeField(null=True),
        ),
    ]