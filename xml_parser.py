import xml.etree.ElementTree as ET
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Transport, Storage, TransportModel, ParserTasks, get_engine, create_session  # Импорт моделей из вашего файла с базой
import unicodedata
import html
import db_updater


def clean_string(s):
    if s is None:
        return ''
    s = html.unescape(s)  # Раскодируем HTML-энтити
    s = unicodedata.normalize('NFKC', s)  # Приводим Unicode-символы к стандарту
    return s.strip().replace('""', '"')  # Удаляем лишние пробелы и заменяем двойные кавычки


def parse_float(value):
    try:
        if value is not None:
            value = value.replace(',', '.')  # Заменяем запятую на точку
        return float(value)
    except (TypeError, ValueError):
        return None

def parse_and_process_xml(xml_data):
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        root = ET.fromstring(xml_data)

        # Проходим по элементам "ДанныеПоЛоту"
        for lot in root.findall('ДанныеПоЛоту'):
            u_number = lot.get('Лот')
            storage_id = int(lot.get('КодСклада').lstrip('0'))
            client = lot.get('Контрагент').strip()
            client = clean_string(client)
            manager = lot.get('ОтветственныйМенеджер')
            latitude = parse_float(lot.get('Широта'))
            longitude = parse_float(lot.get('Долгота'))

            # Проверяем, существует ли машина с данным uNumber
            transport = session.query(Transport).filter_by(uNumber=u_number).first()

            if not transport:
                # Проверяем, существует ли уже задача с таким uNumber и task_name='new_car'
                existing_task = session.query(ParserTasks).filter_by(variable=u_number, task_name='new_car').first()

                if not existing_task:
                    # Если задачи нет, создаем новую задачу
                    new_task = ParserTasks(
                        task_name='new_car',
                        info=ET.tostring(lot, encoding='unicode'),
                        variable=u_number
                    )
                    session.add(new_task)

            else:
                # Проверяем соответствие склада
                storage = session.query(Storage).filter_by(id=transport.storage_id).first()
                if storage.id != storage_id:
                    # Склад отличается, записываем задачу в ParserTasks
                    new_task = ParserTasks(
                        task_name='new_storage',
                        info=ET.tostring(lot, encoding='unicode'),
                        variable=u_number,
                        task_completed=db_updater.update_storage(transport.uNumber, storage_id)
                    )
                    session.add(new_task)
                if transport.manager != manager:
                    # Манагер отличается, записываем задачу в ParserTasks
                    new_task = ParserTasks(
                        task_name='new_client',
                        info=ET.tostring(lot, encoding='unicode'),
                        variable=u_number,
                        task_completed = db_updater.update_manager(transport.uNumber, manager)
                    )
                    session.add(new_task)
                if transport.customer != client:
                    # Клиент отличается, записываем задачу в ParserTasks
                    new_task = ParserTasks(
                        task_name='new_manager',
                        info=ET.tostring(lot, encoding='unicode'),
                        variable=u_number,
                        task_completed = db_updater.update_client(transport.uNumber, client)
                    )
                    session.add(new_task)
                if latitude != 0 or longitude != 0:
                    if transport.x != latitude or transport.y != longitude:
                        # Координаты отличаются, записываем задачу в ParserTasks
                        new_task = ParserTasks(
                            task_name='new_cords',
                            info=ET.tostring(lot, encoding='unicode'),
                            variable=u_number,
                        task_completed = db_updater.update_coordinates(transport.uNumber, latitude, longitude)
                        )
                        session.add(new_task)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка обработки XML: {e}")
    finally:
        session.close()
