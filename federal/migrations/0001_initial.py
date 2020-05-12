# Generated by Django 2.2.10 on 2020-04-28 06:08

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DistrictBoundary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('n_code', models.IntegerField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
            managers=[
                ('vector_tiles', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProvinceBoundary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
            managers=[
                ('vector_tiles', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='GapaNapaBoundary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('cbs_code', models.CharField(blank=True, max_length=100, null=True)),
                ('hlcit_code', models.CharField(blank=True, max_length=100, null=True)),
                ('p_code', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('district_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='District', to='federal.DistrictBoundary')),
                ('province_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Province', to='federal.ProvinceBoundary')),
            ],
            managers=[
                ('vector_tiles', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='districtboundary',
            name='province_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DProvince', to='federal.ProvinceBoundary'),
        ),
    ]