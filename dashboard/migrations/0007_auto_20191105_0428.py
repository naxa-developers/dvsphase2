# Generated by Django 2.0.5 on 2019-11-05 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='type',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]