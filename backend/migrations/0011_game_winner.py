# Generated by Django 2.2.5 on 2019-10-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_game_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
    ]
