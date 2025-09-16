from typing import Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_usd(transactions_: List[Dict[str, Dict[str, Dict[str, str]]]]) -> None:
    # Проверка фильтрации по USD
    result = filter_by_currency(transactions_, "USD")
    for transaction in result:
        assert transaction["operationAmount"]["currency"]["name"] == "USD"


def test_filter_by_currency_rub(transactions_: List[Dict[str, Dict[str, Dict[str, str]]]]) -> None:
    # Проверка фильтрации по USD
    result = filter_by_currency(transactions_, "RUB")
    for transaction in result:
        assert transaction["operationAmount"]["currency"]["name"] == "RUB"


def test_filter_by_currency_try(transactions_: List[Dict[str, Dict[str, Dict[str, str]]]]) -> None:
    # Проверка фильтрации по TRY, транзакции в которой отсутствуют
    try_transactions = filter_by_currency(transactions_, "TRY")
    result = list(try_transactions)
    assert len(result) == 0


def test_empty_list() -> None:
    # Проверка работы с пустым списком
    empty_list: list = []
    result: list = list(filter_by_currency(empty_list, "USD"))
    assert result == []


def test_filter_by_currency_iterator(transactions_: List[Dict[str, Dict[str, Dict[str, str]]]]) -> None:
    # Тест на корректную работу итератора
    iterator = filter_by_currency(transactions_, "USD")
    first = next(iterator)
    second = next(iterator)
    third = next(iterator)

    assert first["id"] == 939719570
    assert second["id"] == 142264268
    assert third["id"] == 895315941


def test_transaction_descriptions(transactions_: list[dict[str, str]]) -> None:
    # Тест на корректную работу итератора
    iterator = transaction_descriptions(transactions_)

    first = next(iterator)
    second = next(iterator)
    third = next(iterator)

    assert first == "Перевод организации"
    assert second == "Перевод со счета на счет"
    assert third == "Перевод со счета на счет"


def test_transaction_descriptions_stop(transactions_: list[dict[str, str]]) -> None:
    # Проверка с вызовом StopIteration
    iterator = transaction_descriptions(transactions_)

    for _ in range(len(transactions_)):
        next(iterator)

    with pytest.raises(StopIteration):
        next(iterator)


def test_transaction_descriptions_empty() -> None:
    # Проверка работы с пустым списком
    empty_list: list = []
    result: list = list(transaction_descriptions(empty_list))
    assert result == []


def test_card_number_generator() -> None:
    # Тест на корректную работу итератора
    gen = card_number_generator(1, 4)
    first = next(gen)
    second = next(gen)
    third = next(gen)
    assert first == "0000 0000 0000 0001"
    assert second == "0000 0000 0000 0002"
    assert third == "0000 0000 0000 0003"


def test_card_number_generator_len_numbers() -> None:
    # Проверка на длину итогового номера
    gen = card_number_generator()
    number = next(gen)
    assert len(number) == 19  # Длина номера 16 цифр плюс три пробела


def test_card_number_generator_limit_value() -> None:
    # Проверка на граничное значение
    gen = card_number_generator(9999999999999999)
    assert next(gen) == "9999 9999 9999 9999"
