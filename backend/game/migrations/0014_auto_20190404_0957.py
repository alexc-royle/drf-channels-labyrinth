# Generated by Django 2.1.4 on 2019-04-04 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20190404_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.IntegerField(choices=[(1, 'lobby'), (2, 'in_progress'), (3, 'completed')], default=1),
        ),
    ]