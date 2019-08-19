from django.db import models

# Create your models here.
class Partner(models.Model):
    partner_name=models.CharField(max_length=100,null=True, blank=True)
    partner_description=models.TextField(blank=True)
    partner_address=models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.partner_name

class MarkerCategory(models.Model):
    marker_category=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.marker_category


class MarkerValues(models.Model):
    marker_category=models.ForeignKey(MarkerCategory, on_delete=models.CASCADE, related_name='MarkerCategory', null=True, blank=True)
    marker_values=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return "{}-{}".format(self.marker_category,self.marker_values)


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
    marker=models.ManyToManyField(MarkerValues,related_name='MarkerValues',blank=True)
    program_code=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.program_name
