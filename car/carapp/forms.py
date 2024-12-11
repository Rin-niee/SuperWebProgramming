#это фильтр(марка авто, модель авто, год от - до, пробег от, км - до, объем от, л - до. тип КПП, привод, цвет)
from django import forms
from .models import Cars, Brands

class CarFilterForm(forms.Form):
    brand = form.ChoseField(choices = [('', 'Бренд')])
