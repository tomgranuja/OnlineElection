# Generated by Django 5.1 on 2025-01-22 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_candidate',
            field=models.BooleanField(default=False, verbose_name='is candidate'),
        ),
    ]
