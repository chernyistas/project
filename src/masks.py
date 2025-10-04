import logging

from pathlib import Path

log_dir = Path('../logs')
log_dir.mkdir(parents=True, exist_ok=True)

# Создаем logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Создаем обработчик для записи в файл
file_handler = logging.FileHandler(
    log_dir / 'masks.log',
    mode='w',
    encoding='utf-8'
)
file_formatter = logging.Formatter('%(asctime)s-%(filename)s-%(levelname)s-%(message)s')
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """Функция принемает  на вход номер карты и возвращает ее маску"""
    logger.info("Начало работы функции")
    # Приводим к строке и убираем пробелы
    logger.info("Функция проверяет на корректность введенные данные")
    card_str = "".join(str(card_number))
    if not card_str:
        logger.error("Номер не может быть пустым")
        raise ValueError("Номер не может быть пустым")

    if not card_str.isdigit():
        logger.error("Неверный формат")
        raise ValueError("Неверный формат")
    logger.info("Функция проверяет количество цифр в карте")
    # Проверяем количество цифр в карте
    if len(card_str) != 16:
        logger.error("Неверное количество цифр")
        raise ValueError("Неверное количество цифр")
    logger.info("Функция формирует маскировочный номер")
    # Формируем маскировочный номер
    masked_card = card_str[:4] + " " + card_str[4:6] + "** ****" + " " + card_str[-4:]
    logger.info("Завершение работы функции")
    return masked_card





def get_mask_account(account_number: int) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""
    logger.info("Начало работы функции")
    # Приводим к строке и убираем пробелы
    logger.info("Функция проверяет на корректность введенные данные")
    account_str = "".join(str(account_number))
    if not account_str:
        raise ValueError("Номер не может быть пустым")
    if not account_str.isdigit():
        raise ValueError("Неверный формат")
    logger.info("Функция проверяет количество цифр в карте")
    # Проверяем количество цифр в карте
    if len(account_str) < 20:
        raise ValueError("Неверное количество цифр")
    logger.info("Функция формирует маскировочный номер")
    # Формируем маскировочный номер
    masked_account = "**" + account_str[-4:]
    logger.info("Завершение работы функции")
    return masked_account
