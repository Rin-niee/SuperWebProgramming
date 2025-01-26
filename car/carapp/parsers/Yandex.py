#https://github.com/useless-apple/yandex_reviews-parser
from yandex_reviews_parser.utils import YandexParser
import json

id_ya = 126455019912  # ID Компании Yandex
parser = YandexParser(id_ya)

all_data = parser.parse()  # Получаем все данные
print(all_data)

# # Выводим только company_reviews
# company_reviews = all_data.get("company_reviews", [])
# print(json.dumps(company_reviews, ensure_ascii=False, indent=2))