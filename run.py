import time
from datetime import datetime
import xml_parser
import exchange
from db_updater import check_status


def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    print("Запуск планировщика задач...")
    while True:
        if check_status() == 0:
            print('Модуль отключен. Ожидание 200 секунд')
            time.sleep(200)
        else:
            xml_data = exchange.check_lot_xml()
            if xml_data is None:
                print(f"{current_time()} | Задач нет")
            else:
                print(f"{current_time()} | Начинаю обработку лотов")
                xml_parser.parse_and_process_xml(xml_data)
                print(f"{current_time()} | Закончил обработку лотов")
            time.sleep(600)
