# Generated by Django 2.2.10 on 2020-04-28 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0111_auto_20200421_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='boundary',
        ),
        migrations.RemoveField(
            model_name='gapanapa',
            name='boundary',
        ),
        migrations.RemoveField(
            model_name='province',
            name='boundary',
        ),
    ]
