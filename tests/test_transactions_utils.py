from unittest.mock import MagicMock, patch

from src.transactions_utils import process_bank_operations, process_bank_search


def test_process_bank_search(data: list[dict]) -> None:
    # Тест 1: Успешный поиск с точным совпадением
    expected = [{"id": 1, "description": "Покупка в магазине"}, {"id": 3, "description": "Покупка в супермаркете"}]

    # Мокаем создание регулярного выражения
    with patch("re.compile") as mock_compile:
        mock_compile.return_value.search = MagicMock(side_effect=[True, False, True])
        result = process_bank_search(data, "покупка")
        assert result == expected


def test_process_bank_search_invalid(data: list[dict]) -> None:
    # Тест 2: Поиск без совпадений
    expected: list = []

    with patch("re.compile") as mock_compile:
        mock_compile.return_value.search = MagicMock(return_value=None)
        result = process_bank_search(data, "несуществующий")
        assert result == expected


def test_process_bank_search_empty() -> None:
    # Тест 3: Поиск с пустыми данными
    expected: list = []

    with patch("re.compile"):
        result = process_bank_search([], "любой")
        assert result == expected


def test_process_bank_operations() -> None:
    # Тест 1: Базовый случай с несколькими категориями
    data = [
        {"description": "food", "amount": 100},
        {"description": "transport", "amount": 200},
        {"description": "food", "amount": 150},
        {"description": "entertainment", "amount": 300},
    ]
    categories = ["food", "transport", "entertainment"]

    expected = {"food": 2, "transport": 1, "entertainment": 1}
    assert process_bank_operations(data, categories) == expected


def test_process_bank_operations_empty() -> None:
    # Тест 2: Пустой список операций
    data: list[dict] = []
    categories = ["food", "transport"]

    expected = {"food": 0, "transport": 0}
    assert process_bank_operations(data, categories) == expected


def test_process_bank_operations_invalid() -> None:
    # Тест 3: Операции не соответствуют категориям
    data = [{"description": "shopping", "amount": 100}, {"description": "bills", "amount": 200}]
    categories = ["food", "transport"]

    expected = {"food": 0, "transport": 0}
    assert process_bank_operations(data, categories) == expected
