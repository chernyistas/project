import json
import logging
import os
from pathlib import Path
from typing import Dict, List

log_dir = Path("../logs")
log_dir.mkdir(parents=True, exist_ok=True)

# Создаем logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Создаем обработчик для записи в файл
file_handler = logging.FileHandler(log_dir / "utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s-%(filename)s-%(levelname)s-%(message)s")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    logger.info("Начало работы функции")
    # Проверяем существование файла
    logger.info("Функция проверяет существование файла")
    if not os.path.exists(file_path):
        print(f"Ошибка: файл '{file_path}' не найден.")
        logger.error(f"Ошибка: файл '{file_path}' не найден.")
        return []

    try:
        # Открываем и считываем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info("Функция открывает и считывает файл")

        # Проверяем, что данные представляют собой список
        logger.info("Функция проверяет, что данные представляют собой список")
        if not isinstance(data, list):
            print("Ошибка: файл не содержит список транзакций.")
            logger.error("Ошибка: файл не содержит список транзакций.")
            return []

        # Проверяем, что элементы списка являются словарями
        logger.info("Функция проверяет, что элементы списка являются словарями")
        for item in data:
            if not isinstance(item, dict):
                print("Ошибка: элементы списка должны быть словарями.")
                logger.error("Ошибка: элементы списка должны быть словарями.")
                return []
        logger.info("Завершение работы функции")
        return data

    except json.JSONDecodeError:
        print("Ошибка: файл содержит некорректный JSON.")
        logger.error("Ошибка: файл содержит некорректный JSON.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        logger.error(f"Произошла ошибка: {str(e)}")
        return []
