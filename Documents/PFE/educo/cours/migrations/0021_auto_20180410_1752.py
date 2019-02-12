# Generated by Django 2.0.4 on 2018-04-10 16:52

import cours.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0020_auto_20180410_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapitres',
            name='fichier',
            field=models.FileField(blank=True, null=True, upload_to=cours.models.file_name_chapitre),
        ),
        migrations.AlterField(
            model_name='chapitres',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=cours.models.image_name_chapitre),
        ),
    ]