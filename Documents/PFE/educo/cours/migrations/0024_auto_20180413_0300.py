# Generated by Django 2.0.4 on 2018-04-13 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0023_auto_20180413_0247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formationssuivis',
            old_name='foramtion',
            new_name='formation',
        ),
    ]
