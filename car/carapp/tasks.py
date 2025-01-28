from celery import shared_task
from django.core.cache import cache
from celery import shared_task
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
import logging
import json
from yandex_reviews_parser.utils import YandexParser
from datetime import datetime
import json
import locale

logger = logging.getLogger(__name__)

@shared_task
def VK_clips():
    clips_data = cache.get('clips_data')
    if clips_data:
        return clips_data
    # Настройка Selenium

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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
    cache.set('clips_data', clips_data, timeout= 60*60*24)
    return clips_data

@shared_task
def Yandex():
    company_reviews = cache.get('company_reviews')
    if company_reviews:
        return company_reviews
    id_ya = 46877748407 #ID Компании Yandex
    parser = YandexParser(id_ya)

    all_data = parser.parse() #Получаем все данные

    # Выводим только company_reviews
    company_reviews = all_data.get("company_reviews", [])
    for review in company_reviews:
        review['stars'] = int(review.get('stars', 0)) if str(review.get('stars', 0)).isdigit() else 0
    
    # locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')  # Для Windows

    for review in company_reviews:
        # Преобразование временной метки
        timestamp = review.get('date', 0)  # Предполагается, что 'date' — это временная метка
        dt_object = datetime.fromtimestamp(timestamp)
        review['formatted_date'] = dt_object.strftime('%d %B %Y г.')
    cache.set('company_reviews', company_reviews, timeout= 60*60*24)
    return company_reviews

