# Generated by Django 2.2.10 on 2020-05-01 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0009_auto_20200501_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='covidspecificprogram',
            name='summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='program', to='covid.CovidSpecificProgramBudget'),
        ),
    ]
