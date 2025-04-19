# log.py

import logging

#logging.basicConfig(
#    level=logging.DEBUG,
#    format="%(asctime)s - %(levelname)s - %(message)s"
#)

logger = logging.getLogger("mybot")
logger.setLevel(logging.INFO)  # можно переключить на DEBUG при необходимости

# Обработчик: лог в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # сюда можно отдельно задать уровень

# Формат логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Подключаем обработчик к логгеру
logger.addHandler(console_handler)
