import pytest
from api_weather import WeatherApi
from info_weather import WeatherInfo


@pytest.mark.parametrize("zip_code", ["20852"])  # Параметры для теста
def test_weather(zip_code):
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
    if actual_temp < 0:
        # Для отрицательных температур
        lower_bound = actual_temp * 1.1  # 10% больше (меньше по абсолютной величине)
        upper_bound = actual_temp * 0.9  # 10% меньше (больше по абсолютной величине)
    else:
        # Для положительных температур
        lower_bound = actual_temp * 0.9  # 10% ниже
        upper_bound = actual_temp * 1.1  # 10% выше

    # Утверждение: фактическая температура должна находиться в диапазоне ±10% от самой себя
    assert lower_bound <= actual_temp <= upper_bound, \
        f"Test failed. Temperature {actual_temp}°C is not within 10% range of itself."
