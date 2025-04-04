import os


class Config:
    VK_API_VERSION = '5.199'
    SECRET_KEY = os.environ.get('Truba1636')  # Замените через настройки окружения на Render.com
    SERVICE_KEY = os.environ.get('380763d6380763d6380763d6bf3b29eca733807380763d65fe9ff71c2fc26f2673d3a56')  # Ваш ключ из ВКонтакте

    @staticmethod
    def validate():
        # Проверка наличия SECRET_KEY
        if Config.SECRET_KEY is None:
            raise ValueError("SECRET_KEY не установлена. Пожалуйста, установите переменную окружения.")

        # Проверка наличия SERVICE_KEY
        if Config.SERVICE_KEY is None:
            raise ValueError("SERVICE_KEY не установлена. Пожалуйста, установите переменную окружения.")