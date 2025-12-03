import logging
import os
import time
from datetime import datetime
import xml_parser
import exchange
from db_updater import check_status


int_level=logging.INFO
if os.getenv('DEV', '0') == '1':
    int_level = logging.DEBUG

logging.basicConfig(
    level=int_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('cm_xml_1c_parser')

if __name__ == "__main__":
    logger.info("Запуск планировщика задач...")
    logger.debug("ВНИМАНИЕ! ЗАПУСК В DEBUG РЕЖИМЕ!")
    while True:
        if check_status() == 0:
            logger.warning('Модуль отключен. Ожидание 200 секунд')
            time.sleep(200)
        else:
            xml_data = exchange.check_lot_xml()
            if xml_data is None:
                logger.info('Задач нет')
            else:
                logger.info('Начинаю обработку лотов')
                xml_parser.parse_and_process_xml(xml_data)
                logger.info('Закончил обработку лотов')
            logger.info('Ожидание 600 секунд')
            time.sleep(600)
