# Generated by Django 2.2.5 on 2019-10-01 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_player_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='start_date',
            new_name='finish_date',
        ),
    ]
