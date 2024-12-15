from django.db import models


class Brands(models.Model):
    country = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    
    class Meta:
        managed = False
        db_table = 'brands'
    def __str__(self):
        return self.brand 


class Cars(models.Model):
    model = models.CharField(max_length=200) #модель
    year = models.IntegerField() #год
    mileage = models.IntegerField() #пробег
    price = models.IntegerField() #цена
    transmission = models.CharField(max_length=200)  #коробка передач
    engine_volume = models.CharField(max_length=2000) #объем двигателя
    drive = models.CharField(max_length=200) #привод
    color = models.CharField(max_length=200) # цвет
    power_volume = models.CharField(max_length=2000) #мощность
    brand_country = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'