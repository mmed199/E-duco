# Generated by Django 2.0.4 on 2018-04-10 16:23

import cours.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0018_contenu_file_image_text_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapitres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('order', cours.fields.OrderField(blank=True)),
                ('contenu', models.TextField(default='')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='cours.Formations')),
            ],
            options={
                'verbose_name': 'Chapitre',
                'ordering': ['order'],
            },
        ),
        migrations.RemoveField(
            model_name='contenu',
            name='contenu_type',
        ),
        migrations.RemoveField(
            model_name='contenu',
            name='module',
        ),
        migrations.RemoveField(
            model_name='file',
            name='utilisateur',
        ),
        migrations.RemoveField(
            model_name='image',
            name='utilisateur',
        ),
        migrations.RemoveField(
            model_name='module',
            name='course',
        ),
        migrations.RemoveField(
            model_name='text',
            name='utilisateur',
        ),
        migrations.RemoveField(
            model_name='video',
            name='utilisateur',
        ),
        migrations.DeleteModel(
            name='Contenu',
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='Module',
        ),
        migrations.DeleteModel(
            name='Text',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
