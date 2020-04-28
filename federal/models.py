from django.contrib.gis.db import models
from rest_framework_mvt.managers import MVTManager


class ProvinceBoundary(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    objects = models.Manager()
    vector_tiles = MVTManager()

    def __str__(self):
        return self.name


class DistrictBoundary(models.Model):
    province_id = models.ForeignKey(ProvinceBoundary, on_delete=models.CASCADE, related_name='DProvince', null=True,
                                    blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    n_code = models.IntegerField(null=True, blank=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    objects = models.Manager()
    vector_tiles = MVTManager()

    def __str__(self):
        return self.name


class GapaNapaBoundary(models.Model):
    province_id = models.ForeignKey(ProvinceBoundary, on_delete=models.CASCADE, related_name='Province', null=True,
                                    blank=True)
    district_id = models.ForeignKey(DistrictBoundary, on_delete=models.CASCADE, related_name='District', null=True,
                                    blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    cbs_code = models.CharField(max_length=100, null=True, blank=True)
    hlcit_code = models.CharField(max_length=100, null=True, blank=True)
    p_code = models.CharField(max_length=100, null=True, blank=True)
    code = models.IntegerField(null=True, blank=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    objects = models.Manager()
    vector_tiles = MVTManager()

    def __str__(self):
        return self.name
