# Generated by Django 2.2.10 on 2020-05-01 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0008_auto_20200430_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidSpecificProgramBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_budget', models.CharField(blank=True, max_length=500, null=True)),
                ('unallocated', models.CharField(blank=True, max_length=500, null=True)),
                ('reported', models.CharField(blank=True, max_length=500, null=True)),
                ('difference', models.CharField(blank=True, max_length=500, null=True)),
                ('percentage_reported', models.CharField(blank=True, max_length=500, null=True)),
                ('percentage_unreported', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='covidspecificprogram',
            name='summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Summary', to='covid.CovidSpecificProgramBudget'),
        ),
    ]
