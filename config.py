import os


class Config:
    VK_API_VERSION = '5.199'
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Замените через настройки окружения на Render.com
    SERVICE_KEY = os.environ.get('SERVICE_KEY')  # Ваш ключ из ВКонтакте

    @staticmethod
    def validate():
        # Проверка наличия SECRET_KEY
        if Config.SECRET_KEY is None:
            raise ValueError("SECRET_KEY не установлена. Пожалуйста, установите переменную окружения.")

        # Проверка наличия SERVICE_KEY
        if Config.SERVICE_KEY is None:
            raise ValueError("SERVICE_KEY не установлена. Пожалуйста, установите переменную окружения.")