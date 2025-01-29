from .forms import *
from .models import *
from .tasks import *
from django.core.cache import cache
from django.db.models import QuerySet

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

def load_models(request):
    brand_id = request.GET.get('brand_id')
    models = Cars.objects.filter(brand_country_id=brand_id).values('model').distinct()
    return JsonResponse(list(models), safe=False)


#Таможенное оформление
def customs_clearance(price, country, KRW, CNY, JPY):
    if country == "Корея":
        price = ((price/1000) * KRW)
    elif country == "Китай":
        price = price * CNY
    else:
        price = ((price/100) * JPY)
    if price<=200000: 
        stavka = 775
    elif 200000 < price <= 450000:
        stavka = 1550
    elif 450000 < price <= 1200000:
        stavka = 3100
    elif 1200000 < price <= 2700000:
        stavka = 8530
    elif 2700000 < price <= 4200000:
        stavka = 12000
    elif 4200000 < price <= 5500000:
        stavka = 15500
    elif 5500000 < price <= 7000000:
        stavka = 20000
    elif 7000000 < price <= 8000000:
        stavka = 23000
    elif 8000000 < price <= 9000000:
        stavka = 25000
    elif 9000000 < price <= 10000000:
        stavka = 27000
    else:
        stavka = 30000
    return stavka

#Единая ставка
def single_rate(price, year_mach, engine_volume, eur, country, KRW, CNY, JPY):
    #перевод в рубли
    if country == "Корея":
        price = ((price/1000) * KRW)
    elif country == "Китай":
        price = price * CNY
    else:
        price = ((price/100) * JPY)
    today_year=datetime.now().year
    year=today_year - year_mach #пробег
    eur_price = price/eur #перевод из рублей в евро
    if year < 3:
        if eur_price <= 8500:
            edin_st=max(54*eur_price/100, 2.5*engine_volume)*eur
        elif 8500 < eur_price <= 16700:
            edin_st=max(48*eur_price/100, 3.5*engine_volume)*eur
        elif 16700 < eur_price <= 42300:
            edin_st=max(48*eur_price/100, 5.5*engine_volume)*eur
        elif 42300 < eur_price <= 84500:
            edin_st=max(48*eur_price/100, 7.5*engine_volume)*eur
        elif 84500 < eur_price <= 169000:
            edin_st=max(48*eur_price/100, 15*engine_volume)*eur
        else:
            edin_st=max(48*eur_price/100, 20*engine_volume)*eur
    elif  3 <= year <= 5:
        if engine_volume <= 1000:
            edin_st=1.5*engine_volume*eur
        elif 1000 < engine_volume <= 1500:
            edin_st=1.7*engine_volume*eur
        elif 1500 < engine_volume <= 1800:
            edin_st=2.5*engine_volume*eur
        elif 1800 < engine_volume <= 2300:
            edin_st=2.7*engine_volume*eur
        elif 2300 < engine_volume <= 2000:
            edin_st=3*engine_volume*eur
        else:
            edin_st=3.6*engine_volume*eur
    else:
        if engine_volume <= 1000:
            edin_st=3*engine_volume*eur
        elif 1000 < engine_volume <= 1500:
            edin_st=3.2*engine_volume*eur
        elif 1500 < engine_volume <= 1800:
            edin_st=3.5*engine_volume*eur
        elif 1800 < engine_volume <= 2300:
            edin_st=4.8*engine_volume*eur
        elif 2300 < engine_volume <= 2000:
            edin_st=5*engine_volume*eur
        else:
            edin_st=5.7*engine_volume*eur
    return edin_st

#Утилизационный сбор
def recycling_collection(year_mach) :
    today_year=datetime.now().year
    year=today_year - year_mach
    if year <= 3:
        recycling = 0.17 * 20000 
    else:
        recycling = 0.26 * 20000 
    return  recycling

# Основной код
def poshlina(price, engine_volume, year_mach, country):
    
    price=int(price)
    engine_volume=int(engine_volume)
    year_mach=int(year_mach)
    currency_data = cache.get('currency_data')# Вызов функции и получение данных курсов валют
    if not currency_data:
        currency_data = fetch_currency_data.delay()
    #вытащить из парсера 
    EUR = float(currency_data.get('EUR', 0))
    KRW = float(currency_data.get('KRW (1000)', 0))  # Используем get для безопасного доступа
    CNY = float(currency_data.get('CNY', 0))
    JPY = float(currency_data.get('JPY (100)', 0))
    
        #обращение к функция для расчета 
    customs = customs_clearance(price,country, KRW, CNY, JPY)
    single = single_rate(price, year_mach, engine_volume, EUR, country, KRW, CNY, JPY)
    recycling = recycling_collection(year_mach)
    total = customs + single + recycling 
    return (int(total))

def add_duties(cars):
    if isinstance(cars, QuerySet):
        for car in cars:
            price = car.price
            engine_volume = car.engine_volume
            year_mach = car.year
            country = car.brand_country.country
            # Рассчитываем пошлину
            total_duty = poshlina(price, engine_volume, year_mach, country)
            # Обновляем поле total
            car.total = total_duty + price
    else:
        price = cars.price
        engine_volume = cars.engine_volume
        year_mach = cars.year
        country = cars.brand_country.country
        # Рассчитываем пошлину
        total_duty = poshlina(price, engine_volume, year_mach, country)
        # Обновляем поле total
        cars.total = total_duty
    return cars
