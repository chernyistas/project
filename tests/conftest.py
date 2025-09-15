import pytest


@pytest.fixture
def card_basic() -> int:
    return 1234567890123456


@pytest.fixture
def account_basic() -> int:
    return 12345678901234567890


@pytest.fixture
def transactions() -> list:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01"},
        {"id": 2, "state": "PENDING", "date": "2023-10-02"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-03"},
        {"id": 4, "state": "FAILED", "date": "2023-10-04"},
        {"id": 5, "state": "EXECUTED", "date": "2023-10-05"},
    ]


@pytest.fixture
def transactions_() -> list:
    return [{
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }]
