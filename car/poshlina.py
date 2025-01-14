import sqlite3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import  By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

#подключение к бд
def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

# Извлечение данных из таблицы car
def get_car_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT price, engine_volume, year FROM cars")
    return cursor.fetchall()


#Таможенное оформление
def customs_clearance(price):

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
def single_rate(price, year_mach, engine_volume, eur):

    today_year=2024
    year=today_year - year_mach #пробег
    eur_price = price/eur #перевод из рублей в евро

    if year <= 3:
        if eur_price <= 8500:
            edin_st=max(54*eur_price, 2.5*engine_volume)*eur
        elif 8500 < eur_price <= 16700:
            edin_st=max(48*eur_price, 3.5*engine_volume)*eur
        elif 16700 < eur_price <= 42300:
            edin_st=max(48*eur_price, 5.5*engine_volume)*eur
        elif 42300 < eur_price <= 84500:
            edin_st=max(48*eur_price, 7.5*engine_volume)*eur
        elif 84500 < eur_price <= 169000:
            edin_st=max(48*eur_price, 15*engine_volume)*eur
        else:
            edin_st=max(48*eur_price, 20*engine_volume)*eur

    elif  3 < year <= 5:
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
def recycling_collection(year_mach):
    today_year=2024
    year=today_year - year_mach
    if year <= 3:
        recycling = 0.17 * 20000 
    else:
        recycling = 0.26 * 20000 

    return  recycling

# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://bbr.ru/")  

# Принять куки
accept_cookies_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='Принять']"))
)
accept_cookies_button.click()

# Развернуть таблицу
expand_table_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-15bdcy0') and contains(., 'Все валюты')]"))
)
expand_table_button.click()

# Нажать на кнопку "Наличный курс"
cash_rate_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'e8slei0') and contains(., 'Наличный курс')]"))
)
cash_rate_button.click()

# Подождать, чтобы таблица успела загрузиться
time.sleep(2)  

# Собрать данные из таблицы
currency_data = {}
rows = driver.find_elements(By.XPATH, "//table[@class='css-1uixtsi e23c5745']//tbody/tr")

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) >= 3:
        currency_code = cells[1].text  # Сокращенное название валюты
        sell_price = cells[4].text      # Цена продажи
        cleaned_price = sell_price.replace(',', '.')
        currency_data[currency_code] = cleaned_price
        
# Закрыть браузер
driver.quit()

# Основной код
def main():
    db_name = 'cars.sqlite3' 
    eur =  float(currency_data['EUR'])# Курс валюты, можно извлечь из базы, если нужно

    conn = connect_to_db(db_name)
    car_data = get_car_data(conn)

    for price_str, engine_volume_str, year_mach_str in car_data:
        # Преобразование строк в целые числа
        price = int(price_str)
        engine_volume = int(engine_volume_str)
        year_mach = int(year_mach_str)

        customs = customs_clearance(price)
        single = single_rate(price, year_mach, engine_volume, eur)
        recycling = recycling_collection(year_mach)
        total = customs + single + recycling #

        print(int(total))

    conn.close()

if __name__ == "__main__":
    main()
