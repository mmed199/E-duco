# Generated by Django 2.0.2 on 2018-03-21 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cours', '0007_profile_utilisateur_date_naissance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='utilisateurs',
            name='utilisateur_email',
        ),
        migrations.RemoveField(
            model_name='utilisateurs',
            name='utilisateur_mdp',
        ),
        migrations.RemoveField(
            model_name='utilisateurs',
            name='utilisateur_valid',
        ),
        migrations.AddField(
            model_name='utilisateurs',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
