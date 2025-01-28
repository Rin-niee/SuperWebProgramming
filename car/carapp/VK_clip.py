
#url = 'https://vk.com/clips/tomiko_trade'

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


# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск в фоновом режиме (без GUI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Загружаем страницу с клипами
driver.get('https://vk.com/clips/tomiko_trade')

# Поиск всех элементов с клипами
clips = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="clip-preview"]')

with open('clips_data.txt', 'w', encoding='utf-8') as file:
    
    #функция поиска ссылок
    for clip in clips:
        url = clip.get_attribute('href')
        preview_image = clip.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        views = clip.find_element(By.CSS_SELECTOR, 'h4[data-testid="clipcontainer-views"]').text

        # Запись данных в файл
        file.write(f'URL: {url}\n')
        file.write(f'Preview Image: {preview_image}\n')
        file.write(f'Views: {views}\n\n')



# Закрываем драйвер
driver.quit()

