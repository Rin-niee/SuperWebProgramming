#перекинуть в расчет пошлины 9

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
        currency_data[currency_code] = sell_price

# Запись данных в файл
with open("currency_data.txt", "w", encoding="utf-8") as file:
    for currency, price in currency_data.items():
        file.write(f"{currency}: {price}\n")

# Закрыть браузер
driver.quit()
