# Generated by Django 2.0.5 on 2019-11-28 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_fivew_project_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProvinceDummy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_id', models.IntegerField(blank=True, null=True)),
                ('geom_char', models.TextField(blank=True, null=True)),
            ],
        ),
    ]