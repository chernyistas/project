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
