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
import re

logger = logging.getLogger(__name__)


@shared_task
def fetch_currency_data():
    currency_data = cache.get('currency_data')
    if currency_data:
        return currency_data
        
    # Настройка Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://bbr.ru/")  

        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Принять']"))
        )
        accept_cookies_button.click()

        eur_sell_price = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='продажа']/following-sibling::div/span"))
        ).text
        eur_sell_price = eur_sell_price.replace(',', '.')

        expand_table_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-15bdcy0') and contains(., 'Все валюты')]"))
        )
        expand_table_button.click()

        time.sleep(2)  

        currency_data = {"EUR": eur_sell_price}

        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[@class='css-1uixtsi e23c5745']//tbody/tr"))
        )
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 3:
                currency_code = cells[1].text
                sell_price = cells[4].text
                cleaned_price = sell_price.replace(',', '.')
                currency_data[currency_code] = cleaned_price
            
    finally:
        driver.quit()
    cache.set('currency_data', currency_data, timeout= 60*60*24)
    return currency_data

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
    reviews = cache.get('reviews')
    if reviews:
        return reviews
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # Открываем страницу с отзывами
        url = "https://yandex.ru/maps/org/tomiko_trade/126455019912/reviews/?ll=131.922567%2C43.127157&z=16"
        driver.get(url)
        # Даем время на загрузку страницы
        time.sleep(1)  # Увеличьте время, если страница загружается медленно
        # Список для хранения отзывов
        reviews = []
        # Поиск всех элементов с отзывами
        review_elements = driver.find_elements(By.CSS_SELECTOR, ".business-reviews-card-view__review")
        for review in review_elements:
            # Извлечение имени пользователя
            author_name = review.find_element(By.CSS_SELECTOR, ".business-review-view__author-name span").text
            # Извлечение иконки пользователя
            avatar_element = review.find_element(By.CSS_SELECTOR,'.business-review-view__author-image .user-icon-view__icon')  # Извлечение URL из стиля
            style = avatar_element.get_attribute('style')
            match = re.search(r'url\("?(.*?)"?\)', style)
            if match:
                avatar_url = match.group(1)
            else:
                avatar_url = None  # Если URL не найден
            # Извлечение количества звезд
            stars = review.find_elements(By.CSS_SELECTOR, ".business-rating-badge-view__star._full")
            star_count = len(stars)
            # Извлечение даты отзыва
            review_date = review.find_element(By.CSS_SELECTOR, ".business-review-view__date span").text
            # Добавление отзыва в список
            reviews.append({
                "name": author_name,
                "icon_href": avatar_url,
                "stars": star_count,
                "date": review_date
            })
        # Закрытие драйвера
        driver.quit()
        cache.set('reviews', reviews, timeout= 60*60*24)
    return reviews

