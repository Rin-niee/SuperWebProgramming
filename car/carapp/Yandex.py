# #https://github.com/useless-apple/yandex_reviews-parser
# from yandex_reviews_parser.utils import YandexParser
# import json
# from selenium import webdriver
# from selenium.common.exceptions import SessionNotCreatedException

# id_ya = 126455019912  # ID Компании Yandex
# parser = YandexParser(id_ya)

# all_data = parser.parse()  # Получаем все данные

# # Выводим только company_reviews
# company_reviews = all_data.get("company_reviews", [])
# print(json.dumps(company_reviews, ensure_ascii=False, indent=2))


import json
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from undetected_chromedriver import Chrome, ChromeOptions

class YandexParser:
    def __init__(self, company_id):
        self.company_id = company_id
        self.driver = None

    def start_driver(self):
        options = ChromeOptions()
        # Добавьте необходимые опции для Chrome, если нужно
        self.driver = Chrome(options=options)

    def parse(self):
        self.start_driver()
        try:
            # Ваш код для парсинга данных с использованием self.driver
            # Например, переход на страницу компании Yandex
            self.driver.get(f"https://yandex.ru/company/{self.company_id}")
            # Здесь должен быть код для извлечения данных

            # Пример извлечения данных
            all_data = {
                "company_reviews": [
                    {"review": "Отличная компания!", "rating": 5},
                    {"review": "Хороший сервис", "rating": 4}
                ]
            }
            return all_data

        except SessionNotCreatedException as e:
            print(f"Ошибка создания сессии: {e}")
            return {}
        finally:
            if self.driver:
                self.driver.quit()  # Убедитесь, что сессия закрыта

if __name__ == "__main__":
    id_ya = 46877748407  # ID Компании Yandex
    parser = YandexParser(id_ya)

    all_data = parser.parse()  # Получаем все данные

    # Выводим только company_reviews
    company_reviews = all_data.get("company_reviews", [])
    print(json.dumps(company_reviews))