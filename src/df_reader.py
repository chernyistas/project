import csv
import logging
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
    Считывает финансовые операции из CSV файла и возвращает список словарей.
    """
    logger.info("Начало работы функции")
    try:

        logger.info(f"Начинаем чтение файла: {file_path}")
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            data = list(reader)  # Преобразуем в список
            logger.info(f"Успешно прочитано {len(data)} записей")
            return data

    except FileNotFoundError:
        logger.info(f"Ошибка: файл {file_path} не найден")
        raise
    except csv.Error as e:
        logger.info(f"Ошибка при чтении CSV файла: {e}")
        raise


def read_transactions_from_excel(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из Excel файла, очищает данные и возвращает список словарей.
    """
    try:
        logger.info(f"Начинаем чтение файла: {file_path}")

        # Читаем файл
        df = pd.read_excel(file_path, sheet_name=0, header=0, engine="openpyxl")
        logger.info(f"Файл успешно прочитан. Строк в файле: {len(df)}")

        # Удаляем строки с NaN:
        df.dropna(inplace=True)

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict(orient="records")
        logger.info("Данные успешно преобразованы в список словарей")
        return transactions

    except FileNotFoundError:
        logger.error(f"Ошибка: файл {file_path} не найден")
        return []

    except Exception as e:
        logger.error(f"Произошла ошибка при чтении файла: {str(e)}")
        return []
