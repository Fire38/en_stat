# Generated by Django 2.2.5 on 2020-12-06 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_game_domen'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]