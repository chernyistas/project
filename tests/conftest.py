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
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
    ]


@pytest.fixture
def transactions_usd() -> list:
    return [{"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}]


@pytest.fixture
def transactions_eur() -> list:
    return [{"operationAmount": {"amount": "50", "currency": {"code": "EUR"}}}]


@pytest.fixture
def transactions_rub() -> list:
    return [{"operationAmount": {"amount": "2000", "currency": {"code": "RUB"}}}]
