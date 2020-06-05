# Generated by Django 2.2.10 on 2020-05-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0116_auto_20200527_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='federal_level',
            field=models.CharField(choices=[('all', 'All'), ('palika', 'Palika Level'), ('district', 'District Level'), ('province', 'Province Level')], default='all', max_length=50),
        ),
    ]