from exchangelib import Credentials, Account, Message, FileAttachment, Configuration, DELEGATE
import config

def check_lot_xml():
    return _check_email(subject="Выгрузка в СЭБ арендного парка и складов.xml", file_name="Выгрузка в СЭБ арендного парка и складов.xml")

def _check_email(subject, file_name):
    """
    Проверяет наличие письма с заданной темой и извлекает XML-файл.
    :param subject: Тема письма, которое ищем.
    :param file_name: Имя XML-файла, которое должно быть в письме.
    :return: Содержимое XML-файла или None, если письмо или файл не найдены.
    """
    # Учетные данные
    mail_config = Configuration(
        server=config.sender_host,
        credentials=Credentials(username=config.full_username, password=config.sender_password)
    )
    account = Account(config.sender_email, config=mail_config, autodiscover=False, access_type=DELEGATE)

    # Поиск письма во входящих
    for folder in account.inbox.walk():
        for item in folder.filter(subject=subject, is_read=False):
            if isinstance(item, Message):
                for attachment in item.attachments:
                    if isinstance(attachment, FileAttachment) and attachment.name == file_name:
                        # Читаем содержимое XML-файла
                        # Пометить письмо как прочитанное
                        item.is_read = True
                        item.save()
                        # Читаем содержимое XML-файла
                        return attachment.content.decode('utf-8')

    return None
