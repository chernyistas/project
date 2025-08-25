import re

import masks


def mask_account_card(account_number: str) -> str:
    """Функция, которая маскирует номер карты или номер счета"""
    # Убираем все кроме букв
    text = re.sub(r"[^а-яА-Яa-zA-Z\s]", "", account_number, flags=re.UNICODE)
    # Убираем все кроме цифр
    digits = re.sub(r"\D", "", account_number)

    # Проверяем есть ли во входящих данных русские буквы
    if re.search("[а-яА-Я]", account_number):
        return str(text + masks.get_mask_account(int(digits)))
    else:
        return str(text + masks.get_mask_card_number(int(digits)))


def get_date(new_date: str) -> str:
    """Функция, которая меняет формат даты"""
    # При помощи срезов в строке меняем дату
    return f"{new_date[8:10]}.{new_date[5:7]}.{new_date[:4]}"
