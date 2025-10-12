import csv
import logging
import os
from pathlib import Path
from typing import Dict, List

import pandas as pd

log_dir = Path("../logs")
log_dir.mkdir(parents=True, exist_ok=True)

# Создаем logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Создаем обработчик для записи в файл
file_handler = logging.FileHandler(log_dir / "df_reader.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s-%(filename)s-%(levelname)s-%(message)s")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def df_csv_transactions(file_path: str) -> List[Dict]:
    """
    Функция для считывания финансовых операций из CSV файла.
    Возвращает список словарей с транзакциями.
    """
    logger.info("Начало работы функции")

    # Проверка существования файла
    logger.info("Проверка существования файла")
    if not os.path.exists(file_path):
        logger.error(f"Файл '{file_path}' не найден")
        return []

    try:
        # Открытие и чтение файла
        logger.info("Открытие и чтение файла")
        with open(file_path, "r", encoding="utf-8") as file:
            # Используем csv.DictReader с указанием разделителя
            reader = csv.DictReader(file, delimiter=";")
            transactions = []  # Список для хранения транзакций

            # Проходим по всем строкам файла
            for row in reader:
                # Создаем словарь с транзакцией
                transaction = {
                    "id": row.get("id"),
                    "state": row.get("state"),
                    "date": row.get("date"),
                    "amount": row.get("amount"),
                    "currency_name": row.get("currency_name"),
                    "currency_code": row.get("currency_code"),
                    "from": row.get("from"),
                    "to": row.get("to"),
                    "description": row.get("description"),
                }
                transactions.append(transaction)

                # Проверка элементов списка
        logger.info("Проверка элементов списка")
        for item in transactions:
            if not isinstance(item, dict):
                logger.error("Элементы списка должны быть словарями")
                return []

        logger.info("Завершение работы функции")
        return transactions

    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        return []


# print(df_csv_transactions('../data/transactions.csv'))
def read_transactions_from_excel(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из Excel файла и возвращает список словарей.
    """
    try:
        # Открываем файл и читаем данные
        excel_data = pd.read_excel(file_path, engine="openpyxl")

        # Проверяем наличие всех необходимых столбцов
        required_columns = [
            "id",
            "state",
            "date",
            "amount",
            "currency_name",
            "currency_code",
            "from",
            "to",
            "description",
        ]

        if not all(column in excel_data.columns for column in required_columns):
            logging.error("Отсутствуют необходимые столбцы в файле")
            raise ValueError("В файле отсутствуют необходимые столбцы")

        # Преобразуем DataFrame в список словарей
        transactions = excel_data.to_dict(orient="records")

        # Валидируем данные в каждой транзакции
        for transaction in transactions:
            if not isinstance(transaction["id"], (int, float)):
                raise ValueError("Неверный формат ID транзакции")
            if not isinstance(transaction["amount"], (int, float)):
                raise ValueError("Неверная сумма транзакции")

        logging.info(f"Успешно прочитано {len(transactions)} транзакций")
        return transactions

    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден")
        print(f"Ошибка: файл {file_path} не найден")
        return []

    except pd.errors.EmptyDataError:
        logging.warning("Прочитан пустой файл")
        print("Файл пуст")
        return []

    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")
        print(f"Произошла ошибка при чтении файла: {str(e)}")
        return []


print(read_transactions_from_excel("../data/transactions_excel.xlsx"))
