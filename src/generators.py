def filter_by_currency(transactions: list, currency: str) -> iter:
    """Возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной"""
    # Проверяем валюту операции
    for transaction in transactions:
        if transaction['operationAmount']['currency']['name'] == currency:
            yield transaction


def transaction_descriptions(transactions: list) -> iter:
    """Возвращает итератор, который поочередно выдает описание транзакции"""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start=1, end=9999999999999999):
    """Генератор, который выдает номера банковских карт в формате
XXXX XXXX XXXX XXXX, где X — цифра номера карты"""
    # Форматируем число, добавляя ведущие нули и пробелы
    current = start
    while current <= end:
        formatted_number = f"{current:016d}"
        yield (f"{formatted_number[:4]} {formatted_number[4:8]} "
               f"{formatted_number[8:12]} {formatted_number[12:]}")
        current += 1
