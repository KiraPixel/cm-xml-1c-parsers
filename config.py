import os

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', 'sqlite:///default.db')
MAIL_MAIL = os.getenv('MAIL_MAIL', 'aboba@aboba.ru')
MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'aboba')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '1q2w3e4r5t6y')
