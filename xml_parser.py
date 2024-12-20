import xml.etree.ElementTree as ET
from idlelib.pyparse import trans

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

        #Проходим по элементам "ДанныеПоЛоту"
        for lot in root.findall('ДанныеПоЛоту'):
            u_number = lot.get('Лот')
            storage_id = int(lot.get('КодСклада').lstrip('0'))
            client = lot.get('Контрагент').strip()
            client = clean_string(client)
            transport_model = lot.get('ИДМодели')
            manager = lot.get('ОтветственныйМенеджер')
            latitude = parse_float(lot.get('Широта'))
            longitude = parse_float(lot.get('Долгота'))

            # Проверяем, существует ли машина с данным uNumber
            transport = session.query(Transport).filter_by(uNumber=u_number).first()

            if not transport:
                # Проверяем, существует ли уже задача с таким uNumber и task_name='new_car'
                db_updater.add_task('new_car', lot, u_number)
            else:
                # Проверяем соответствие склада
                storage = session.query(Storage).filter_by(id=transport.storage_id).first()
                if storage.id != storage_id:
                    # Склад отличается, записываем задачу в ParserTasks
                    db_updater.add_task('new_storage', lot, u_number, db_updater.update_storage(transport.uNumber, storage_id))
                if transport.model_id != transport_model:
                    # Модель ТС отличается, записываем задачу в ParserTasks
                    db_updater.add_task('transport_model_change', lot, u_number, db_updater.update_transport(transport.uNumber, transport_model))
                if transport.manager != manager:
                    # Манагер отличается, записываем задачу в ParserTasks
                    db_updater.add_task('new_manager', lot, u_number, db_updater.update_manager(transport.uNumber, manager))
                if transport.customer != client:
                    # Клиент отличается, записываем задачу в ParserTasks
                    db_updater.add_task('new_client', lot, u_number, db_updater.update_client(transport.uNumber, client))
                if latitude != 0 or longitude != 0:
                    if transport.x != latitude or transport.y != longitude:
                        # Координаты отличаются, записываем задачу в ParserTasks
                        db_updater.add_task('new_cords', lot, u_number, db_updater.update_coordinates(transport.uNumber, latitude, longitude))


        for storage_element in root.findall('ДанныеПоСкладу'):
            storage_id = int(storage_element.get('ИДСклада').lstrip('0'))
            storage_name = storage_element.get('Наименование').strip()
            storage_type = storage_element.get('ТипСклада')
            region = storage_element.get('Регион')
            address = parse_float(storage_element.get('Адрес'))
            organization = parse_float(storage_element.get('Организация'))

            storage_query = session.query(Storage).filter_by(id=storage_id).first()

            if not storage_query:
                new_task = ParserTasks(
                    task_name='new_storage',
                    info=ET.tostring(storage_element, encoding='unicode'),
                    variable=storage_id
                )
                session.add(new_task)
                db_updater.create_new_storage(storage_id, storage_name, storage_type, region, address, organization)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка обработки XML: {e}")
    finally:
        session.close()
