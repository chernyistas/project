from datetime import datetime

import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(transactions: list) -> None:
    filtered = filter_by_state(transactions, "EXECUTED")
    assert len(filtered) == 3
    assert all(transaction["state"] == "EXECUTED" for transaction in filtered)


def test_sort_by_date_ascending(transactions: list) -> None:
    sorted_transactions = sort_by_date(transactions, ascending=True)
    dates = [datetime.fromisoformat(t["date"]) for t in sorted_transactions]
    assert dates == sorted(dates)


def test_sort_by_date_descending(transactions: list) -> None:
    sorted_transactions = sort_by_date(transactions, ascending=False)
    dates = [datetime.fromisoformat(t["date"]) for t in sorted_transactions]
    assert dates == sorted(dates, reverse=True)


# Проверка обработки исключений
def test_invalid_date_format(transactions: list) -> None:
    transactions[0]["date"] = "invalid_date"
    with pytest.raises(ValueError):
        sort_by_date(transactions)


def test_missing_state(transactions: list) -> None:
    del transactions[0]["state"]
    with pytest.raises(KeyError):
        filter_by_state(transactions)
