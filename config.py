import os

class Config:
    VK_API_VERSION = '5.199'
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Заменить через Heroku
    SERVICE_KEY = os.environ.get('SERVICE_KEY') # Ваш ключ из ВК