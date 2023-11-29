class WeatherInfo:
    def __init__(self, data):
        # Инициализация с данными о погоде
        self.data = data

    def get_temperature(self):
        # Возвращает текущую температуру из данных погоды
        return self.data.get('main', {}).get('temp')
