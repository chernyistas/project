def get_mask_card_number(card_number: int) -> str:
    """Функция принемает  на вход номер карты и возвращает ее маску"""
    # Приводим к строке и убираем пробелы
    card_str = "".join(str(card_number))
    # Формируем маскировочный номер
    masked_card = card_str[:4] + " " + card_str[4:6] + "** ****" + " " + card_str[-4:]
    return masked_card


def get_mask_account(account_number: int) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""
    # Приводим к строке и убираем пробелы
    account_str = "".join(str(account_number))
    # Формируем маскировочный номер
    masked_account = "**" + account_str[-4:]
    return masked_account
