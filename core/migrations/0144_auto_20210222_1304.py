# Generated by Django 2.2.10 on 2021-02-22 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0143_auto_20210222_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='partner_id',
            field=models.ManyToManyField(related_name='Progpartner', to='core.Partner'),
        ),
    ]
