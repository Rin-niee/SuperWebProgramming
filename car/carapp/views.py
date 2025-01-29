from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import *
from yandex_reviews_parser.utils import YandexParser
from datetime import datetime
import json
import locale
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import  By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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


# def fetch_currency_data():

#     # Настройка Selenium
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     try:
#         driver.get("https://bbr.ru/")  

#         # Принять куки
#         accept_cookies_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[text()='Принять']"))
#         )
#         accept_cookies_button.click()



#         # Достать цену продажи евро
#         eur_sell_price = WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//span[text()='продажа']/following-sibling::div/span"))
#         ).text
#         eur_sell_price = eur_sell_price.replace(',', '.')

#         #достать азиатскую валюту
#         # Развернуть таблицу
#         expand_table_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-15bdcy0') and contains(., 'Все валюты')]"))
#         )
#         expand_table_button.click()

#         # Подождать, чтобы таблица успела загрузиться
#         time.sleep(2)  

#         # Собрать данные из таблицы
#         currency_data = {}
#         rows = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.XPATH, "//table[@class='css-1uixtsi e23c5745']//tbody/tr"))
#         )
#         for row in rows:
#             cells = row.find_elements(By.TAG_NAME, "td")
#             if len(cells) >= 3:
#                 currency_code = cells[1].text  # Сокращенное название валюты
#                 sell_price = cells[4].text      # Цена продажи
#                 cleaned_price = sell_price.replace(',', '.')
#                 currency_data[currency_code] = cleaned_price
            
#     finally:
#         # Закрыть браузер
#         driver.quit()
#     return eur_sell_price, currency_data



# Основной код
def main(price, engine_volume, year_mach, country):
    # db_name = 'cars.sqlite3'
    
    price=int(price)
    engine_volume=int(engine_volume)
    year_mach=int(year_mach)
    #eur, currency_data = fetch_currency_data()  # Вызов функции и получение данных курсов валют
    eur =  107.20#float(eur)

    #вытащить из парсера 
    KRW = 109.00 #float(currency_data.get('KRW (1000)', 0))  # Используем get для безопасного доступа
    CNY = 14.10#float(currency_data.get('CNY', 0))
    JPY = 71.69 #float(currency_data.get('JPY (100)', 0))
    
    
    # conn = connect_to_db(db_name)
    # car_data = get_car_data(conn)

    #вытаскиваются из базы 
    # for price_str, engine_volume_str, year_mach_str, brand_country_id in car_data:
    #     # Преобразование строк в целые числа
    #     price = int(price_str)
    #     engine_volume = int(engine_volume_str)
    #     year_mach = int(year_mach_str)

    #      # Получение названия страны
    #     country = get_country_by_brand_id(conn, brand_country_id)

        #обращение к функция для расчета 
    customs = customs_clearance(price,country, KRW, CNY, JPY)
    single = single_rate(price, year_mach, engine_volume, eur, country, KRW, CNY, JPY)
    recycling = recycling_collection(year_mach)
    total = customs + single + recycling 

    return (int(total))

    # conn.close()
# x = main(1200000, 660, 2022, 'Корея')
# print(x)
def add_duties(cars):
    for car in cars:
        price = car.price
        engine_volume = car.engine_volume
        year_mach = car.year
        country = car.brand_country.country

        # Рассчитываем пошлину
        total_duty = main(price, engine_volume, year_mach, country)

        # Обновляем поле total
        car.total = total_duty
    return cars


# def VK_clips():
#     # Настройка Selenium
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     # Загружаем страницу с клипами
#     driver.get('https://vk.com/clips/tomiko_trade')

#     # Поиск всех элементов с клипами
#     clips = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="clip-preview"]')

#     clips_data = []  # Список для хранения данных клипов

#     # Функция поиска ссылок
#     for clip in clips:
#         url = clip.get_attribute('href')
#         preview_image = clip.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
#         views = clip.find_element(By.CSS_SELECTOR, 'h4[data-testid="clipcontainer-views"]').text

#         # Создание словаря для каждого клипа
#         clip_info = {
#             'url': url,
#             'preview_image': preview_image,
#             'views': views
#         }
        
#         # Добавление словаря в список
#         clips_data.append(clip_info)

#     # Закрываем драйвер
#     driver.quit()
    
#     return clips_data


# def Yandex():
    
#     id_ya = 46877748407 #ID Компании Yandex
#     parser = YandexParser(id_ya)

#     all_data = parser.parse() #Получаем все данные

#     # Выводим только company_reviews
#     company_reviews = all_data.get("company_reviews", [])
#     return company_reviews


# Create your views here.
def get_country_name_in_case(country, case='nominative'):
    # Словарь с названиями стран и их формами в разных падежах
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
            form.save()  # Сохраняем данные в базе данных
            return JsonResponse({'success': True, 'message': 'Форма успешно отправлена!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return forms

def index(request):
    forms = contact(request)
    carsmini = Cars.objects.all()
    # reviews = Yandex()[:6]
    # for review in reviews:
    #     review['stars'] = int(review.get('stars', 0)) if str(review.get('stars', 0)).isdigit() else 0
    
    # locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')  # Для Windows

    # for review in reviews:
    #     # Преобразование временной метки
    #     timestamp = review.get('date', 0)  # Предполагается, что 'date' — это временная метка
    #     dt_object = datetime.fromtimestamp(timestamp)
    #     review['formatted_date'] = dt_object.strftime('%d %B %Y г.')
    # star_range = range(5)
        

    # Отфильтруйте автомобили по странам
    cars_japan = carsmini.filter(brand_country__country='Япония')[:5]
    cars_korea = carsmini.filter(brand_country__country='Корея')[:5]
    cars_china = carsmini.filter(brand_country__country='Китай')[:5]

    # clips = VK_clips()
    # clips = clips[:8]
    # Передайте отфильтрованные данные в шаблон

    # Рассчитываем пошлину для каждой группы автомобилей
    cars_japan = add_duties(cars_japan)
    cars_japan = add_duties(cars_korea)
    cars_japan = add_duties(cars_china)
    # Передайте отфильтрованные данные в шаблон

    context = {
        # 'clips': clips,
        'forms': forms,
        'cars_japan': cars_japan,
        'cars_korea': cars_korea,
        'cars_china': cars_china,
        # 'reviews': reviews,
        # 'star_range': star_range,
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
    # Применяем сортировку, если параметр сортировки передан
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
    
    cars = add_duties(cars)

    paginator = Paginator(cars, 12)  # Показывать по 12 машин на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-запроса
    try:
        cars_page = paginator.page(page_number)  # Получаем нужную страницу
    except PageNotAnInteger:
        cars_page = paginator.page(1)  # Если номер страницы не является целым числом, показываем первую
    except EmptyPage:
        cars_page = paginator.page(paginator.num_pages)  # Если номер страницы больше, чем количество страниц, показываем последнюю
    forms = contact(request)
    carsmini= Cars.objects.filter(brand_country__country=country)[:5]
    carsmini = add_duties(carsmini)
    context = {
        'country_forms': get_country_name_in_case(country = country, case = 'genitive'),
        'country': country,
        'form': form,
        'cars': cars,
        'cars_page': cars_page,
        'carsmini': carsmini,
        'forms': forms,
        'sort_choices': SORT_CHOICES,  # Передаем варианты сортировки в шаблон
        'current_sort': sort_option,  # Текущая выбранная сортировка
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