# Generated by Django 2.2.10 on 2020-04-28 07:42

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('federal', '0002_auto_20200428_1326'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='provinceboundary',
            managers=[
                ('vector_tiles', django.db.models.manager.Manager()),
            ],
        ),
    ]
