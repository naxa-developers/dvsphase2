# Generated by Django 3.2 on 2024-03-19 04:09

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0177_alter_feedbackform_your_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name_en', models.CharField(blank=True, max_length=500, null=True)),
                ('name_ne', models.CharField(blank=True, max_length=500, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeatureCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attr_data', models.JSONField(default=dict)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name_en', models.CharField(blank=True, max_length=500, null=True)),
                ('name_ne', models.CharField(blank=True, max_length=500, null=True)),
                ('layer_type', models.CharField(blank=True, choices=[('raster', 'Raster'), ('vector', 'Vector'), ('wms', 'WMS')], max_length=15, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VectorLayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('file_upload', models.FileField(blank=True, null=True, upload_to='layer/vectorlayer_uploads')),
                ('type_of_layer', models.CharField(blank=True, choices=[('Shapefile', 'Shapefile'), ('Geojson', 'Geojson'), ('CSV', 'CSV'), ('KML', 'KML'), ('Raster', 'Raster'), ('OSM', 'OSM'), ('WMS', 'WMS')], max_length=20, null=True)),
                ('lat_field', models.CharField(blank=True, max_length=250, null=True)),
                ('long_field', models.CharField(blank=True, max_length=250, null=True)),
                ('geometry_type', models.CharField(blank=True, max_length=250, null=True)),
                ('bbox', models.JSONField(blank=True, default=dict, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('layer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vector_layer', to='core.layer')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='GisStyle',
        ),
        migrations.AddField(
            model_name='featurecollection',
            name='feature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_data', to='core.vectorlayer'),
        ),
    ]
