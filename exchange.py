from exchangelib import Credentials, Account, Message, FileAttachment
import config

def check_lot_xml():
    return _check_email(subject="Выгрузка по арендным лотам/складам.xml", file_name="Выгрузка по арендным лотамскладам.xml")

def _check_email(subject, file_name):
    """
    Проверяет наличие письма с заданной темой и извлекает XML-файл.
    :param subject: Тема письма, которое ищем.
    :param file_name: Имя XML-файла, которое должно быть в письме.
    :return: Содержимое XML-файла или None, если письмо или файл не найдены.
    """
    # Учетные данные
    credentials = Credentials(config.MAIL_USERNAME, config.MAIL_PASSWORD)
    account = Account(config.MAIL_MAIL, credentials=credentials, autodiscover=True)

    # Поиск письма во входящих
    for item in account.inbox.filter(subject=subject, is_read=False):
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
