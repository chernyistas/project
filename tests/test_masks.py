import pytest

from src.masks import get_mask_account, get_mask_card_number


# Базовые тест
def test_get_mask_card_number_basic(card_basic: int) -> None:
    assert get_mask_card_number(card_basic) == "1234 56** **** 3456"
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"


# Граничные случаи
def test_get_mask_card_number_limit() -> None:
    assert get_mask_card_number(9999999999999999) == "9999 99** **** 9999"


def test_get_mask_card_number_start_limit() -> None:
    assert get_mask_card_number(1111111111111111) == "1111 11** **** 1111"


# Проверка с некорректными значениями
@pytest.mark.parametrize(
    "card_number, expected_error_message",
    [
        ("", "Номер не может быть пустым"),  # Пустая строка
        (129876, "Неверное количество цифр"),  # Слишком короткий номер
        ("123asdsafa99876a", "Неверный формат"),  # Символы, не являющиеся цифрами
    ],
)
def test_get_mask_card_number(card_number: int, expected_error_message: str) -> None:
    with pytest.raises(ValueError) as e:
        get_mask_account(card_number)

        # Проверяем, что сообщение об ошибке совпадает с ожидаемым
    assert str(e.value) == expected_error_message


# Базовые тест
def test_get_mask_account_basic(account_basic: int) -> None:
    assert get_mask_account(account_basic) == "**7890"


# Граничные случаи
def test_get_mask_account_start_limit() -> None:
    assert get_mask_account(99999999999999999999) == "**9999"


def test_get_mask_account_limit() -> None:
    assert get_mask_account(11111111111111111111) == "**1111"


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("", ValueError),  # Пустая строка
        (123456789009876, ValueError),  # Слишком короткий номер
        (1234567890098764234722, ValueError),  # Слишком длинный номер
        ("1234567890ыф6a", ValueError),  # Символы, не являющиеся цифрами
    ],
)
def test_get_mask_account(account_number: int, expected: bool) -> None:
    if isinstance(expected, Exception):
        with pytest.raises(expected):
            get_mask_account(account_number)
