# Generated by Django 2.1.4 on 2019-01-11 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20190111_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamepiece',
            name='orientation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.GamePieceOrientation'),
        ),
    ]