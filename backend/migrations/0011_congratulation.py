# Generated by Django 2.2.5 on 2019-12-30 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20191202_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Congratulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('text', models.CharField(max_length=2000)),
            ],
        ),
    ]