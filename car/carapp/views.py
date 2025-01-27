from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from yandex_reviews_parser.utils import YandexParser
# import json
from django.http import JsonResponse
from .models import *
from .forms import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeDriverManager
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def VK_clips(browser="chrome"):
    # Настройка Selenium
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.headless = True  # Запуск в фоновом режиме
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
        driver = webdriver.Edge(service=EdgeService(EdgeDriverManager().install()), options=options)

    else:
        raise ValueError("Неподдерживаемый браузер")

    # Загружаем страницу с клипами
    driver.get('https://vk.com/clips/tomiko_trade')

    # Поиск всех элементов с клипами
    clips = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="clip-preview"]')

    clips_data = []  # Список для хранения данных клипов

    # Функция поиска ссылок
    for clip in clips:
        url = clip.get_attribute('href')
        preview_image = clip.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        views = clip.find_element(By.CSS_SELECTOR, 'h4[data-testid="clipcontainer-views"]').text

        # Создание словаря для каждого клипа
        clip_info = {
            'url': url,
            'preview_image': preview_image,
            'views': views
        }
        
        # Добавление словаря в список
        clips_data.append(clip_info)

    # Закрываем драйвер
    driver.quit()
    
    return clips_data



# Create your views here.

#это чтобы получить разные конечности
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

#это функция для принятия контакта(она есть везде)

def contact(request):
    if request.method == 'POST':
        form = Connection(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Форма успешно отправлена!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return forms

# #это для яндекса
# def OTZIVI():
#     id_ya = 126455019912  # ID Компании Yandex
#     parser = YandexParser(id_ya)

#     all_data = parser.parse()  # Получаем все данные

#     # Выводим только company_reviews
#     company_reviews = all_data.get("company_reviews", [])
#     return all_data.get("company_reviews", [])

def index(request):
    forms = contact(request)
    carsmini = Cars.objects.all()

    cars_japan = carsmini.filter(brand_country__country='Япония')[:5]
    cars_korea = carsmini.filter(brand_country__country='Корея')[:5]
    cars_china = carsmini.filter(brand_country__country='Китай')[:5]
    # company_reviews = OTZIVI()
    clips = VK_clips()
    clips = clips[:8]
    context = {
        'clips': clips,
        'forms': forms,
        'cars_japan': cars_japan,
        'cars_korea': cars_korea,
        'cars_china': cars_china,
        # 'company_reviews': company_reviews,
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