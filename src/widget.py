import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_number: str) -> str:
    """Функция, которая маскирует номер карты или номер счета"""
    if not account_number:
        raise ValueError("Пустая строка")
    # Убираем все кроме букв
    text = re.sub(r"[^а-яА-Яa-zA-Z\s]", "", account_number, flags=re.UNICODE)
    # Убираем все кроме цифр
    digits = re.sub(r"\D", "", account_number)
    if len(digits) < 16 or len(digits) > 19:
        raise ValueError("Некорректная длина номера")

    # Проверяем есть ли во входящих данных русские буквы
    if re.search("[а-яА-Я]", account_number):
        return str(text + get_mask_account(int(digits)))
    else:
        return str(text + get_mask_card_number(int(digits)))
    # Проверяем длину номера


def get_date(new_date: str) -> str:
    """Функция, которая меняет формат даты"""
    # При помощи срезов в строке меняем дату
    return f"{new_date[8:10]}.{new_date[5:7]}.{new_date[:4]}"
