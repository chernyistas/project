from unittest.mock import MagicMock, patch

from src.transactions_utils import process_bank_search


def test_process_bank_search(data: list[dict]) -> None:
    # Тест 1: Успешный поиск с точным совпадением
    expected = [{"id": 1, "description": "Покупка в магазине"}, {"id": 3, "description": "Покупка в супермаркете"}]

    # Мокаем создание регулярного выражения
    with patch("re.compile") as mock_compile:
        mock_compile.return_value.search = MagicMock(side_effect=[True, False, True])
        result = process_bank_search(data, "покупка")
        assert result == expected, "Тест 1 не пройден"


def test_process_bank_search_invalid(data: list[dict]) -> None:
    # Тест 2: Поиск без совпадений
    expected: list = []

    with patch("re.compile") as mock_compile:
        mock_compile.return_value.search = MagicMock(return_value=None)
        result = process_bank_search(data, "несуществующий")
        assert result == expected, "Тест 2 не пройден"


def test_process_bank_search_empty() -> None:
    # Тест 3: Поиск с пустыми данными
    expected: list = []

    with patch("re.compile"):
        result = process_bank_search([], "любой")
        assert result == expected, "Тест 3 не пройден"
