# Generated by Django 2.1.4 on 2019-04-05 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20190405_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='currentplayer', to='game.UserCounter'),
        ),
    ]
