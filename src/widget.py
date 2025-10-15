import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_number: str) -> str:
    """Функция, которая маскирует номер карты или номер счета"""
    # Проверяем, что строка не пустая
    if not account_number:
        raise ValueError("Пустая строка")

    # Разделяем текст и цифры
    account_number = str(account_number)
    account_number = account_number.strip()
    text = re.sub(r"[^а-яА-Яa-zA-Z\s]", "", account_number, flags=re.UNICODE).strip()
    digits = re.sub(r"\D", "", account_number)

    # Проверяем корректность длины номера
    if len(digits) < 16 or len(digits) > 20:
        raise ValueError("Некорректная длина номера")

    # Определяем тип маскировки
    if "счет" in account_number.lower():
        masked_number = get_mask_account(digits)
    else:
        masked_number = get_mask_card_number(digits)

    # Формируем итоговый результат
    if text:
        return f"{text} {masked_number}"
    return masked_number


def get_date(new_date: str) -> str:
    """Функция, которая меняет формат даты"""
    if "Z" in new_date:
        date_format = "%Y-%m-%dT%H:%M:%SZ"
    elif "." in new_date:
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
    else:
        raise ValueError("Неподдерживаемый формат даты")

        # Парсим дату
    date_obj = datetime.strptime(new_date, date_format)

    # Форматируем в нужный вид
    return date_obj.strftime("%d.%m.%Y")
