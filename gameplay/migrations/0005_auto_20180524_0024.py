# Generated by Django 2.0.4 on 2018-05-23 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0004_auto_20180422_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='by_first_player',
            field=models.BooleanField(editable=False),
        ),
    ]