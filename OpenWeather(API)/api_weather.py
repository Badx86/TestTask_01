import json
from logger import Logger
import requests
from decouple import config


class WeatherApi:
    """
    Класс для взаимодействия с API погоды OpenWeatherMap
    """
    def __init__(self):
        """
        Инициализация API с использованием ключа API из переменных окружения
        """
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = config("API_KEY")

    def get_weather_by_zipcode(self, zip_code):
        """
        Получение погоды по почтовому индексу

        :param zip_code: Почтовый индекс для запроса погоды
        :return: Ответ API в формате JSON или None в случае ошибки
        """
        params = {
            'zip': f"{zip_code},us",
            'appid': self.api_key,
            'units': 'metric',
        }
        url = f"{self.base_url}"
        try:
            Logger.add_request(url, params, headers=None, cookies=None, method='GET')  # Логирование запроса
            response = requests.get(url, params=params)
            response.raise_for_status()
            Logger.add_response(response)  # Логирование ответа
            print(json.dumps(response.json(), indent=4, ensure_ascii=False))
            return response.json()
        except requests.RequestException as e:
            Logger.add_response(e.response) if e.response else Logger._write_log_to_file(f"Request failed: {e}\n")
            print(f"Error during API request: {e}")
            return None
