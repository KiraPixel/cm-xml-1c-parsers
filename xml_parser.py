import xml.etree.ElementTree as ET
from idlelib.pyparse import trans
from tabnanny import check

from sqlalchemy.orm import sessionmaker
from models import Transport, Storage, TransportModel, ParserTasks, get_engine, create_session  # Импорт моделей из вашего файла с базой
import unicodedata
import html
import db_updater
import api_cm


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
    engine = db_updater.engine
    session = create_session(engine)

    try:
        root = ET.fromstring(xml_data)

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


        all_transports = session.query(Transport.uNumber).all()
        transport_numbers_in_db = {t[0] for t in all_transports}

        #Проходим по элементам "ДанныеПоЛоту"
        for lot in root.findall('ДанныеПоЛоту'):
            u_number = lot.get('Лот')
            storage_id = int(lot.get('КодСклада').lstrip('0'))
            client = lot.get('Контрагент').strip()
            client = clean_string(client)
            transport_model = lot.get('ИДМодели')
            transport_vin = lot.get('Серия')
            transport_year = lot.get('СерияГодВыпуска')
            manager = lot.get('ОтветственныйМенеджер')
            latitude = parse_float(lot.get('Широта'))
            longitude = parse_float(lot.get('Долгота'))
            if latitude is None or longitude is None:
                latitude = 0
                longitude = 0

            # Проверяем, существует ли машина с данным uNumber
            transport = session.query(Transport).filter_by(uNumber=u_number).first()


            if not transport:
                success = 0
                request_to_api = api_cm.add_new_car(u_number, transport_model, storage_id, transport_vin,
                                   transport_year, client, manager, latitude, longitude, 0)
                if request_to_api == 'ok':
                    success = 1
                    print(f'Новая машина {u_number} успешно добавлена')
                db_updater.add_task('new_car', lot, u_number, success)
                continue

            transport_numbers_in_db.discard(u_number)

            # хардкод против спамящий ТС
            if transport.uNumber in ['E 01815']:
                continue

            transport.parser_1c = 1
            session.commit()

            if transport.storage_id != storage_id:
                # Склад отличается, записываем задачу в ParserTasks
                db_updater.add_task('new_storage', lot, u_number, db_updater.update_storage(transport.uNumber, storage_id))
            if transport.model_id != transport_model:
                # Модель ТС отличается, записываем задачу в ParserTasks
                db_updater.add_task('transport_model_change', lot, u_number, db_updater.update_transport(transport.uNumber, transport_model))
            if transport.vin != transport_vin:
                # VIN отличается, записываем задачу в ParserTasks
                db_updater.add_task('new_vin', lot, u_number, db_updater.update_vin(transport.uNumber, transport_vin))
            if transport.manufacture_year != transport_year:
                # Год ТС отличается, записываем задачу в ParserTasks
                db_updater.add_task('new_manufacture_year', lot, u_number, db_updater.update_manufacture_year(transport.uNumber, transport_year))
            if transport.manager != manager:
                # Манагер отличается, записываем задачу в ParserTasks
                db_updater.add_task('new_manager', lot, u_number, db_updater.update_manager(transport.uNumber, manager))
            if transport.customer != client:
                # Клиент отличается, записываем задачу в ParserTasks
                db_updater.add_task('new_client', lot, u_number, db_updater.update_client(transport.uNumber, client))
            if transport.x != latitude or transport.y != longitude:
                #print(f'cords: {transport.x} != {latitude} or {transport.y} != {longitude}')
                # Координаты отличаются, записываем задачу в ParserTasks
                db_updater.add_task('new_cords', lot, u_number, db_updater.update_coordinates(transport.uNumber, latitude, longitude))
            session.commit()

        if transport_numbers_in_db:
            session.query(Transport).filter(Transport.uNumber.in_(transport_numbers_in_db)).update(
                {Transport.parser_1c: 0}, synchronize_session=False
            )
        session.commit()

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка обработки XML: {e}")
    finally:
        session.close()
