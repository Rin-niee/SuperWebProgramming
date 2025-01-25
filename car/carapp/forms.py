#это фильтр(марка авто, модель авто, год от - до, пробег от, км - до, объем от, л - до. тип КПП(коробка передач), привод, цвет)
from django import forms
from .models import *

class CarFilterForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brands.objects.none(), required=False)
    model = forms.ChoiceField(choices=[], required=False)
    year_from = forms.ChoiceField(choices=[], required=False)
    year_to= forms.ChoiceField(choices=[], required=False)
    mileage_from = forms.ChoiceField(choices=[], required=False)
    mileage_to = forms.ChoiceField(choices=[], required=False)
    engine_volume_from = forms.ChoiceField(choices=[], required=False)
    engine_volume_to = forms.ChoiceField(choices=[], required=False)
    transmission = forms.ChoiceField(choices=[], required=False)
    drive = forms.ChoiceField(choices=[], required=False)
    color = forms.ChoiceField(choices=[], required=False)
    
    def __init__(self, *args, **kwargs):
        country = kwargs.pop('country', None)
        super(CarFilterForm, self).__init__(*args, **kwargs)
        
        if country:
            #это для бренда
            self.fields['brand'].queryset = Brands.objects.filter(country=country)
            #это для модели
            self.fields['model'].choices = [(model, model) for model in sorted(set(car.model for car in Cars.objects.filter(brand_country__country=country)))]
            self.fields['year_from'].choices = [(year, year) for year in sorted(set(car.year for car in Cars.objects.filter()))]
            self.fields['year_to'].choices = [(year, year) for year in sorted(set(car.year for car in Cars.objects.filter()))]
            self.fields['mileage_from'].choices = [(mileage, mileage) for mileage in sorted(set(car.mileage for car in Cars.objects.filter()))]
            self.fields['mileage_to'].choices = [(mileage, mileage) for mileage in sorted(set(car.mileage for car in Cars.objects.filter()))]
            self.fields['engine_volume_from'].choices = [(engine_volume, engine_volume) for engine_volume in sorted(set(car.engine_volume for car in Cars.objects.filter()))]
            self.fields['engine_volume_to'].choices = [(engine_volume, engine_volume) for engine_volume in sorted(set(car.engine_volume for car in Cars.objects.filter()))]
            self.fields['transmission'].choices = [(transmission, transmission) for transmission in set(car.transmission for car in Cars.objects.filter())]
            self.fields['drive'].choices = [(drive, drive) for drive in set(car.drive for car in Cars.objects.filter())]
            self.fields['color'].choices = [(color, color) for color in set(car.color for car in Cars.objects.filter()) if color]




class Connection(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = Contact
        fields = 'name' , 'number', 'message'
    check = forms.BooleanField(required=True)