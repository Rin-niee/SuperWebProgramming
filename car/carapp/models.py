from django.db import models


class brand(models.Model):
    country = models.CharField()
    brand = models.CharField()

    class Meta:
        managed = False
        db_table = 'brands'


class cars(models.Model):
    model = models.CharField()
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.IntegerField()
    transmission = models.CharField()
    engine_volume = models.CharField()
    drive = models.CharField()
    color = models.CharField()
    power_volume = models.CharField()
    brand_country = models.ForeignKey(brand, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'