# Generated by Django 2.0.5 on 2019-12-04 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_provincedummy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fivew',
            name='representative_person',
        ),
    ]
