# Generated by Django 5.1.6 on 2025-03-06 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0008_user_photo_profil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('client', 'Client'), ('collecteur', 'Collecteur'), ('agent', 'Agent de réception')], default='collecteur', max_length=20),
        ),
    ]
