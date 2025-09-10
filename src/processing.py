from datetime import datetime


def filter_by_state(transaction_list: list, state: str = "EXECUTED") -> list:
    """Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению."""
    return [transaction for transaction in transaction_list if transaction["state"] == state]


def sort_by_date(transaction_list: list, ascending: bool = True) -> list:
    """Функция возвращает новый список, отсортированный по дате"""
    return sorted(transaction_list, key=lambda x: datetime.fromisoformat(x["date"]), reverse=not ascending)
