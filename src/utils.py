import json
import os
from typing import Dict, List


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    # Проверяем существование файла
    if not os.path.exists(file_path):
        print(f"Ошибка: файл '{file_path}' не найден.")
        return []

    try:
        # Открываем и считываем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные представляют собой список
        if not isinstance(data, list):
            print("Ошибка: файл не содержит список транзакций.")
            return []

        # Проверяем, что элементы списка являются словарями
        for item in data:
            if not isinstance(item, dict):
                print("Ошибка: элементы списка должны быть словарями.")
                return []

        return data

    except json.JSONDecodeError:
        print("Ошибка: файл содержит некорректный JSON.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return []
