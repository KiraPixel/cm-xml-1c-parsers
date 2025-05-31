import os

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', 'sqlite:///default.db')

sender_email = os.getenv('MAIL_MAIL', 'nomail@nomail')
sender_user = os.getenv('MAIL_USERNAME', 'user')
sender_domain = os.getenv('MAIL_USERNAME_DOMAIN', 'mail')
sender_password = os.getenv('MAIL_PASSWORD', 'password')
sender_host = os.getenv('MAIL_HOST', 'mail.ru')
use_domain_format = os.getenv('USE_DOMAIN_FORMAT', 'at')
full_username = ''

if use_domain_format == 'backslash':
    full_username = f"{sender_domain}\\{sender_user}"
else:
    full_username = f"{sender_user}@{sender_domain}"