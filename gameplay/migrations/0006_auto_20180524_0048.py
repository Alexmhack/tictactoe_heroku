# Generated by Django 2.0.4 on 2018-05-23 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0005_auto_20180524_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='by_first_player',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AlterField(
            model_name='move',
            name='game',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='gameplay.Game'),
        ),
    ]
