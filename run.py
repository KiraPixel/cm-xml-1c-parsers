import time
from datetime import datetime
import xml_parser
import exchange
from db_updater import reset_parser_1c

def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main():
    while True:

        # Проверяем XML-данные
        xml_data = exchange.check_lot_xml()

        if xml_data is None:
            print(f"{current_time()} | Задач нет")
        else:
            print(f"{current_time()} | Начинаю обработку лотов")
            xml_parser.parse_and_process_xml(xml_data)
            reset_parser_1c()
            print(f"{current_time()} | Закончил обработку лотов")

        # Ждем 10 минут
        time.sleep(600)

if __name__ == "__main__":
    print('xml-1c-parser Started')
    main()
