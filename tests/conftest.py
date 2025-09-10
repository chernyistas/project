import pytest


@pytest.fixture
def card_basic() -> int:
    return 1234567890123456


@pytest.fixture
def account_basic() -> int:
    return 12345678901234567890
