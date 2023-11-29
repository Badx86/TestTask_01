import pytest
from api_weather import WeatherApi
from info_weather import WeatherInfo


@pytest.mark.parametrize("zip_code, expected_temp", [("20852", 3.4)])  # Параметры для теста
def test_weather(zip_code, expected_temp):
    # Создание экземпляра WeatherApi и получение данных о погоде
    weather_api = WeatherApi()
    weather_data = weather_api.get_weather_by_zipcode(zip_code)

    # Утверждение: данные о погоде должны быть получены
    assert weather_data is not None, "Failed to retrieve weather data."

    # Создание экземпляра WeatherInfo и получение текущей температуры
    weather_info = WeatherInfo(weather_data)
    actual_temp = weather_info.get_temperature()

    # Утверждение: температура должна быть в ответе
    assert actual_temp is not None, "Temperature not found in response."

    # Вычисление допустимого диапазона температур
    lower_bound = expected_temp * 0.9  # 10% ниже
    upper_bound = expected_temp * 1.1  # 10% выше

    # Утверждение: фактическая температура должна находиться в диапазоне ±10% от ожидаемой
    assert lower_bound <= actual_temp <= upper_bound, \
        f"Test failed. Temperature {actual_temp}°C is not within 10% range of expected temperature {expected_temp}°C."
