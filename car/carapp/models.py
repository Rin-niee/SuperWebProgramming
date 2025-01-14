from django.db import models
from django.core.validators import RegexValidator

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

class Contact(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть в формате: '+999999999'. Максимально допустимое количество цифр - 15.")

    name = models.CharField(max_length=255, verbose_name='Имя заказчика')
    number = models.CharField(max_length=12, unique=True, verbose_name='Номер телефона', validators=[phone_regex])
    message = models.TextField(blank=True, verbose_name='текст обращения')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        managed = True
        db_table = 'contact' 
    def __str__(self):
        return self.name 
