from django.shortcuts import render
from django.http import HttpResponse
from .models import Cars, Brands


# Create your views here.
def index(request):
    return render(request, 'index.html')

def catalog(request, country):
    # Здесь вы можете написать логику для фильтрации автомобилей по стране,
    # Если вы хотите, например, получить список автомобилей этой страны:
    cars = Cars.objects.filter(brand_country_id__country=country)  # предположим, что в вашей модели Car есть ForeignKey с моделью Brand
    brands = Brands.objects.filter(country = country)
    # Теперь передаем country и cars в контекст
    context = {
        'country': country,
        'cars': cars,
        'brands': brands
    }

    return render(request, 'catalog.html', context)
def auto(request):
    return render(request, 'auto.html')

def promotion(request):
    return render(request, 'promotion.html')

def contacts(request):
    return render(request, 'contacts.html')

def workconditions(request):
    return render(request, 'workconditions.html')
