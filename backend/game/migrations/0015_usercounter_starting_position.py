# Generated by Django 2.1.4 on 2019-04-05 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_auto_20190404_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercounter',
            name='starting_position',
            field=models.IntegerField(choices=[(1, 'top_left'), (7, 'top_right'), (43, 'bottom_left'), (49, 'bottom_right')], null=True),
        ),
    ]