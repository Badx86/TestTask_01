import datetime
import json
import os
from requests import Response


class Logger:
    """
    Класс для логирования информации о запросах и ответах
    """
    file_name = f"logs/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    @classmethod
    def _write_log_to_file(cls, data: str):
        """
        Запись логов в файл
        :param data: Строка, содержащая информацию для логирования
        """
        # Убедимся, что директория logs существует перед записью в файл
        logs_dir = os.path.dirname(cls.file_name)
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        """
        Добавление информации о запросе в лог
        :param url: URL запроса
        :param data: Данные запроса
        :param headers: Заголовки запроса
        :param cookies: Cookies запроса
        :param method: HTTP метод (GET, POST, и т.д.)
        """
        # Получение имени текущего теста из переменных окружения
        testname = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        """
        Добавление информации об ответе в лог
        :param response: Объект ответа (response) от библиотеки requests
        """
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        # Форматирование текста ответа в виде отформатированного JSON
        data_to_add += f"Response text: {json.dumps(response.json(), indent=4, ensure_ascii=False)}\n"
        # Форматирование заголовков ответа с использованием отступов
        headers_formatted = '\n'.join(f"{key}: {value}" for key, value in headers_as_dict.items())
        data_to_add += f"Response headers:\n{headers_formatted}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += f"\n-----\n"

        cls._write_log_to_file(data_to_add)
