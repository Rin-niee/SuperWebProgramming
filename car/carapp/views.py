from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = Connection(request.POST)
        if form.is_valid():
            form.save()
            form = Connection()
    else: 
        form = Connection()
    context = {
        'forms': form
    }
    return render(request, 'index.html', context)

def catalog(request, country):
    cars = Cars.objects.filter(brand_country__country=country)
    if request.method == 'GET':
        form = CarFilterForm(request.GET, country=country)
        if form.is_valid():
            brand = form.cleaned_data.get('brand')
            model = form.cleaned_data.get('model')
            year_from = form.cleaned_data.get('year_from')
            year_to = form.cleaned_data.get('year_to')
            mileage_from = form.cleaned_data.get('mileage_from')
            mileage_to = form.cleaned_data.get('mileage_to')
            engine_volume_from = form.cleaned_data.get('engine_volume_from')
            engine_volume_to = form.cleaned_data.get('engine_volume_to')
            transmission = form.cleaned_data.get('transmission')
            drive = form.cleaned_data.get('drive')
            color = form.cleaned_data.get('color')
            if brand:
                cars = cars.filter(brand_country=brand)
            if model:
                cars = cars.filter(model=model)
            #года
            if year_from:
                cars = cars.filter(year__gte=year_from)
            if year_to:
                cars = cars.filter(year__lte=year_to)
            if year_from and year_to:
                cars = cars.filter(year__range=(year_from, year_to))
            #хз что это
            if mileage_from:
                cars = cars.filter(mileage__gte=mileage_from)    
            if mileage_to:
                cars = cars.filter(mileage__lte=mileage_to)
                
            if mileage_from and mileage_to:
                cars = cars.filter(mileage__range=(mileage_from, mileage_to))
            #объем двигателя
            if engine_volume_from:
                cars = cars.filter(engine_volume__gte=engine_volume_from)
            if engine_volume_to:
                cars = cars.filter(engine_volume__lte=engine_volume_to)
            if engine_volume_from and engine_volume_to:
                cars = cars.filter(engine_volume__range=(engine_volume_from, engine_volume_to))
            
            if transmission:
                cars = cars.filter(transmission=transmission)
            if drive:
                cars = cars.filter(drive=drive)
            if color:
                cars = cars.filter(color=color)
    context = {
        'country': country,
        'form': form,
        'cars': cars
    }
    return render(request, 'catalog.html', context)
    
def auto(request, car_id):
    car = Cars.objects.filter(id=car_id)
    context = {
        'car': car,
        'id':car_id
    }
    return render(request, 'auto.html', context)

def promotion(request):
    return render(request, 'promotion.html')

def contacts(request):
    return render(request, 'contacts.html')

def workconditions(request):
    return render(request, 'workconditions.html')
