# Generated by Django 2.1.4 on 2019-01-09 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_basegamepiece_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basegamepiece',
            name='title',
        ),
    ]
