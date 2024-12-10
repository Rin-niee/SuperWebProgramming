from django.db import models


class Brands(models.Model):
    country = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    
    class Meta:
        managed = False
        db_table = 'brands'


class Cars(models.Model):
    model = models.CharField(max_length=200)
    year = models.IntegerField(max_length=200)
    mileage = models.IntegerField(max_length=200)
    price = models.IntegerField(max_length=200)
    transmission = models.CharField(max_length=200)
    engine_volume = models.CharField(max_length=200)
    drive = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    power_volume = models.CharField(max_length=200)
    brand_country = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'