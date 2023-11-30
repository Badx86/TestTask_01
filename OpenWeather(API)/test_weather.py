import pytest
from datetime import datetime
from api_weather import WeatherApi
from info_weather import WeatherInfo

# Минимальная и максимальная температура за 2022 год,
# источник: https://www.accuweather.com/en/us/rockville/20850/november-weather/329305
# Словарь с историческими диапазонами температур по месяцам за 2022 год:
historical_monthly_temps = {
    1: {'min': -13, 'max': 16},
    2: {'min': -12, 'max': 22},
    3: {'min': -9, 'max': 24},
    4: {'min': -1, 'max': 30},
    5: {'min': 2, 'max': 34},
    6: {'min': 8, 'max': 34},
    7: {'min': 16, 'max': 36},
    8: {'min': 13, 'max': 36},
    9: {'min': 8, 'max': 32},
    10: {'min': -2, 'max': 25},
    11: {'min': -8, 'max': 26},
    12: {'min': -16, 'max': 16},
}


@pytest.mark.parametrize("zip_code", ["20852"])  # Параметры для теста
def test_weather(zip_code):
    current_month = datetime.now().month
    expected_temp_range = historical_monthly_temps.get(current_month)

    assert expected_temp_range is not None, f"No historical data for month {current_month}"

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

    # Рассчитываем допустимый диапазон температур с учетом 10% колебаний
    if expected_temp_range['min'] < 0:
        adjusted_min_temp = expected_temp_range['min'] * 1.1  # 10% ниже для отрицательной температуры
    else:
        adjusted_min_temp = expected_temp_range['min'] * 0.9  # 10% ниже для положительной температуры

    if expected_temp_range['max'] < 0:
        adjusted_max_temp = expected_temp_range['max'] * 0.9  # 10% выше для отрицательной температуры
    else:
        adjusted_max_temp = expected_temp_range['max'] * 1.1  # 10% выше для положительной температуры

    # Утверждение: фактическая температура должна находиться в пределах допустимого диапазона
    assert adjusted_min_temp <= actual_temp <= adjusted_max_temp, \
        (f"Test failed. Current temperature {actual_temp}°C is not within the expected range "
         f"for month {current_month}: {adjusted_min_temp}°C - {adjusted_max_temp}°C.")
