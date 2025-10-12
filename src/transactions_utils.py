import logging
import re
from pathlib import Path

log_dir = Path("../logs")
log_dir.mkdir(parents=True, exist_ok=True)

# Создаем logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Создаем обработчик для записи в файл
file_handler = logging.FileHandler(log_dir / "transactions_utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s-%(filename)s-%(levelname)s-%(message)s")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Функция для поиска операций по строке в описании"""
    try:
        logger.info(f"Начато выполнение поиска. Строка поиска: {search}")

        # Создаем шаблон регулярного выражения
        pattern = re.compile(search, re.IGNORECASE)
        logger.info(f"Создано регулярное выражение: {pattern.pattern}")
        # Фильтруем операции
        result = []
        for transaction in data:
            logger.info(f"Проверка транзакции: {transaction}")
            # Проверяем наличие искомой строки в описании операции
            if "description" in transaction:
                if pattern.search(transaction["description"]):
                    result.append(transaction)
                    logger.info(f"Найдено совпадение: {transaction}")
            else:
                logger.warning(f"Транзакция без описания: {transaction}")

        logger.info(f"Найдено {len(result)} совпадений")
        return result

    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        raise

#
#
# data = [
#     {
#         'id': 1,
#         'amount': 1000,
#         'date': '2023-10-01',
#         'description': 'Оплата в магазине продуктов'
#     },
#     {
#         'id': 2,
#         'amount': 500,
#         'date': '2023-10-02',
#         'description': 'Перевод другу'
#     },
#     {
#         'id': 3,
#         'amount': 2000,
#         'date': '2023-10-03',
#         'description': 'Покупка в продуктовом магазине'
#     }
# ]
# found_transactions = process_bank_search(data, 'пере')
# print(found_transactions)
