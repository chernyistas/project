import re
import masks


def mask_account_card(account_number: str) -> str:
    """Функция, которая маскирует номер карты или номер счета"""
    # Убираем все кроме букв
    text = re.sub(r'[^а-яА-Яa-zA-Z\s]', '', account_number, flags=re.UNICODE)
    # Убираем все кроме цифр
    digits = re.sub(r'\D', '', account_number)

    # Проверяем есть ли во входящих данных русские буквы
    if re.search("[а-яА-Я]", account_number):
        return text + masks.get_mask_account(int(digits))
    else:
        return text + masks.get_mask_card_number(int(digits))


card_number = "Счет 73654108430135874305"
print(mask_account_card(card_number))


# Visa Platinum 7000792289606361  # входной аргумент
# Visa Platinum 7000 79** **** 6361  # выход функции
# Счет 73654108430135874305  # входной аргумент
# Счет **4305  # выход функции
#
def get_date(new_date: str) -> str:
    """Функция, которая меняет формат даты"""
    # При помощи срезов в строке меняем дату
    return f"{new_date[8:10]}.{new_date[5:7]}.{new_date[:4]}"


date = "2024-03-11T02:26:18.671407"
print(get_date("2024-03-11T02:26:18.671407"))
# # В том же модуле создайте функцию  get_date, которая принимает на вход строку с датой в формате
# # "2024-03-11T02:26:18.671407" и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024").
