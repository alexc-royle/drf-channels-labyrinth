# Generated by Django 2.1.4 on 2019-01-11 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_game_gamepiece_usercounter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamepiece',
            name='collectable_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.CollectableItem'),
        ),
    ]