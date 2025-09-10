import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_basic(card_basic: int) -> None:
    assert get_mask_card_number(card_basic) == "1234 56** **** 3456"  # Обычный случай


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("", ValueError),  # Пустая строка
        (129876, ValueError),  # Слишком короткий номер
        (6543212313212130098764234722, ValueError),  # Слишком длинный номер
        ("123asdsafa99876a", ValueError),  # Символы, не являющиеся цифрами
    ],
)
def test_get_mask_card_number(card_number: int, expected: bool) -> None:
    if isinstance(expected, Exception):
        with pytest.raises(expected):
            get_mask_account(card_number)


def test_get_mask_account_basic(account_basic: int) -> None:
    assert get_mask_account(account_basic) == "**7890"  # Обычный случай


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
