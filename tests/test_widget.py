import pytest

from src.widget import get_date, mask_account_card


# Тесты для функции mask_account_card
@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ],
)
def test_mask_account_card(input_data: str, expected_output: bool) -> None:
    result = mask_account_card(input_data)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("123456789012345", "123456789012345"),  # Некорректная длина
        ("abcdefghijklmno", "abcdefghijklmno"),  # Только буквы
        ("12345678901234567890", "12345678901234567890"),  # Слишком длинный номер
        ("", ""),  # Пустая строка
        (" ", " "),  # Строка с пробелами
        ("**Счет", "**Счет"),  # Нет номера счета
        ("Maestro", "Maestro"),  # Нет номера карты
        ("Счет 1234567890123456", "Счет **3456"),  # Короткий номер счета
    ],
)
def test_mask_account_card_invalid(input_data: str, expected_output: bool) -> None:
    with pytest.raises(ValueError):
        mask_account_card(input_data)


@pytest.mark.parametrize(
    "input_date, expected_output",
    [
        ("2023-10-05", "05.10.2023"),  # Стандартная дата
        ("1999-12-31", "31.12.1999"),  # Конец года
        ("2000-01-01", "01.01.2000"),  # Начало года
        ("0001-01-01", "01.01.0001"),  # Минимальная дата
        ("9999-12-31", "31.12.9999"),  # Максимальная дата
    ],
)
def test_get_date(input_date: str, expected_output: str) -> None:
    """Тестирование функции get_date с корректными входными данными."""
    result = get_date(input_date)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_date",
    [
        "2023-13-01",  # Некорректный месяц
        "2023-02-30",  # Некорректный день
        "2023-10-05T12:00:00",  # Формат с временем
    ],
)
def test_get_date_invalid_input(input_date: str) -> None:
    """Тестирование функции get_date с некорректными входными данными."""
    with pytest.raises(ValueError):
        get_date(input_date)
