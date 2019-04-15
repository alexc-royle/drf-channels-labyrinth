# Generated by Django 2.1.4 on 2019-04-04 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20190118_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='current_player',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.IntegerField(choices=[(1, 'Lobby'), (2, 'In Progress'), (3, 'Completed')], default=1),
        ),
        migrations.AddField(
            model_name='usercounter',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]