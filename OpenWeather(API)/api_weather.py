import json

import requests
from decouple import config


class WeatherApi:
    def __init__(self):
        # Основной URL для API погоды и ключ API, полученный из переменных окружения
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = config("API_KEY")

    def get_weather_by_zipcode(self, zip_code):
        # Параметры запроса, включая почтовый индекс и ключ API.
        # Используется единица измерения 'metric' для получения температуры в градусах Цельсия
        params = {
            'zip': f"{zip_code},us",
            'appid': self.api_key,
            'units': 'metric',
        }
        try:
            # Отправка запроса к API
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Проверка на ошибки запроса
            print(json.dumps(response.json(), indent=4, ensure_ascii=False))  # Вывод ответа API
            return response.json()
        except requests.RequestException as e:
            # Обработка возможных ошибок запроса
            print(f"Error during API request: {e}")
            return None
