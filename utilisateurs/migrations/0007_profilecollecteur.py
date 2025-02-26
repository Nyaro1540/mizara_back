# Generated by Django 5.1.6 on 2025-02-19 13:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0006_remove_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileCollecteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nif', models.CharField(max_length=9, unique=True, verbose_name="Numéro d'Identification Fiscale")),
                ('stat', models.CharField(max_length=8, unique=True, verbose_name='Numéro STAT')),
                ('cin', models.CharField(max_length=9, unique=True, verbose_name="Carte d'Identité Nationale")),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_collecteur', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profil Collecteur',
                'verbose_name_plural': 'Profils Collecteurs',
            },
        ),
    ]
