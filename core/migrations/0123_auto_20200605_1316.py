# Generated by Django 2.2.10 on 2020-06-05 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0122_auto_20200604_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
