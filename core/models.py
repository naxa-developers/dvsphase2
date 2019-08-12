from django.db import models

# Create your models here.
class Organization(models.Model):
    organization_name=models.CharField(max_length=100,null=True, blank=True)
    organization_description=models.TextField(blank=True)
    organization_address=models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.organization_name

class MarkerCategory(models.Model):
    Marker_category=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.Marker_category


class MarkerValues(models.Model):
    marker_category=models.ForeignKey(MarkerCategory, on_delete=models.CASCADE, related_name='MarkerCategory', null=True, blank=True)
    marekr_values=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return "{}-{}".format(self.marker_category,self.marekr_values)


class Sector(models.Model):
    sector_name=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.sector_name



class SubSector(models.Model):
    sector=models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='Sector', null=True, blank=True)
    sub_sector_name=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.sub_sector_name




class Program(models.Model):
    program_name=models.CharField(max_length=100,null=True, blank=True)
    program_description=models.TextField(blank=True)
    sub_sector=models.ForeignKey(SubSector, on_delete=models.CASCADE, related_name='SubSector', null=True, blank=True)
    marker=models.ManyToManyField(MarkerValues,related_name='MarkerValues', null=True, blank=True)

    def __str__(self):
        return self.program_name
