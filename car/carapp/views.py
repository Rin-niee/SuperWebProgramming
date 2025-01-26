from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import *



# Create your views here.
def get_country_name_in_case(country, case='nominative'):
    country_forms = {
        'Корея': {
            'nominative': 'Корея',
            'genitive': 'Кореи',
        },
        'Япония': {
            'nominative': 'США',
            'genitive': 'Японии',
        },
        'Китай': {
            'nominative': 'Китай',
            'genitive': 'Китая',
        },
    }
    
    return country_forms.get(country, {}).get(case, country)


def contact(request):
    if request.method == 'POST':
        form = Connection(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Форма успешно отправлена!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return forms

def index(request):
    forms = contact(request)
    carsmini = Cars.objects.all()

    cars_japan = carsmini.filter(brand_country__country='Япония')[:5]
    cars_korea = carsmini.filter(brand_country__country='Корея')[:5]
    cars_china = carsmini.filter(brand_country__country='Китай')[:5]
    context = {
        'forms': forms,
        'cars_japan': cars_japan,
        'cars_korea': cars_korea,
        'cars_china': cars_china,
    }
    return render(request, 'index.html', context)


SORT_CHOICES = {
    'mileage_asc': ('mileage', 'Пробег (по возрастанию)'),
    'mileage_desc': ('-mileage', 'Пробег (по убыванию)'),
    'price_asc': ('price', 'Цена (по возрастанию)'),
    'price_desc': ('-price', 'Цена (по убыванию)'),
    'engine_volume_asc': ('engine_volume', 'Объем двигателя (по возрастанию)'),
    'engine_volume_desc': ('-engine_volume', 'Объем двигателя (по убыванию)'),
    'year_asc': ('year', 'Год (по возрастанию)'),
    'year_desc': ('-year', 'Год (по убыванию)'),
}

def catalog(request, country):
    cars = Cars.objects.filter(brand_country__country=country)
    sort_option = request.GET.get('sort')
    if sort_option in SORT_CHOICES:
        cars = cars.order_by(SORT_CHOICES[sort_option][0])  # Сортировка по полю из SORT_CHOICES
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

    paginator = Paginator(cars, 12)
    page_number = request.GET.get('page')
    try:
        cars_page = paginator.page(page_number)
    except PageNotAnInteger:
        cars_page = paginator.page(1)
    except EmptyPage:
        cars_page = paginator.page(paginator.num_pages)
    forms = contact(request)
    carsmini= Cars.objects.filter(brand_country__country=country)[:5]
    context = {
        'country_forms': get_country_name_in_case(country = country, case = 'genitive'),
        'country': country,
        'form': form,
        'cars': cars,
        'cars_page': cars_page,
        'carsmini': carsmini,
        'forms': forms,
        'sort_choices': SORT_CHOICES,
        'current_sort': sort_option,
    }
    return render(request, 'catalog.html', context)

def load_models(request):
    brand_id = request.GET.get('brand_id')
    models = Cars.objects.filter(brand_country_id=brand_id).values('model').distinct()
    return JsonResponse(list(models), safe=False)
    
def auto(request, car_id):
    car = Cars.objects.filter(id=car_id)
    country = Cars.objects.select_related('brand_country').get(id=car_id)
    countryid = country.brand_country.country
    forms = contact(request)
    carsmini= Cars.objects.filter(brand_country__country=countryid)[:5]
    context = {
        'country_forms': get_country_name_in_case(country = countryid, case = 'genitive'),  
        'carsmini': carsmini,
        'car': car,
        'id':car_id,
        'forms': forms,
       
    }
    return render(request, 'auto.html', context)

def promotion(request):
    forms = contact(request)
    context = {
        'forms': forms,
    }
    return render(request, 'promotion.html', context)

def contacts(request):
    forms = contact(request)
    context = {
        'forms': forms,
    }
    return render(request, 'contacts.html', context)

def workconditions(request):
    forms = contact(request)
    context = {
        'forms': forms,
    }
    return render(request, 'workconditions.html', context)

# def get_models(request):
#     brand_id = request.GET.get('brands_id')
#     if brand_id:
#         models = Cars.objects.filter(brand_id=brand_id).values('model').distinct()
#         model_choices = [(model['model'], model['model']) for model in models]
#     return JsonResponse({'models': []})