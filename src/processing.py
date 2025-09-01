from datetime import datetime


def filter_by_state(list_dicts: list, state: str = 'EXECUTED') -> list:
    """Функция возвращает словари с ключом по умолчанию"""
    return [list_dict for list_dict in list_dicts if list_dict["state"] == 'EXECUTED']


def sort_by_date(list_dicts: list, reverse: bool = True) -> list:
    """Функция сортирует список по дате"""
    return sorted(list_dicts, key=lambda x: datetime.fromisoformat(x['date']), reverse=reverse)
