import os
from typing import Dict, List

import requests
from dotenv import load_dotenv

# Загрузка переменных из .env-файла
load_dotenv()

API_KEY = os.getenv("API_KEY")


def transaction_amount(transactions: List[Dict]) -> float:
    """
    Функция конвертации валюты из USD и EUR в рубли.
    Принимает список транзакций и возвращает сумму в рублях.
    """
    code_rub = "RUB"
    total_amount = 0.0  # Общая сумма в рублях

    for transaction in transactions:
        try:
            # Извлекаем сумму и валюту из транзакции
            amount = transaction["operationAmount"]["amount"]
            currency = transaction["operationAmount"]["currency"]["code"]

            # Если транзакция уже в рублях — добавляем к общей сумме
            if currency == code_rub:
                total_amount += float(amount)
                continue

            # Формируем URL для запроса к API
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={code_rub}&from={currency}&amount={amount}"
            headers = {"apikey": API_KEY}

            # Делаем запрос к API
            response = requests.get(url, headers=headers)

            # Проверяем статус ответа
            if response.status_code != 200:
                raise Exception(f"Ошибка API: {response.status_code}")

            # Парсим JSON и получаем конвертированную сумму
            data = response.json()
            converted_amount = data.get("result")

            # Добавляем конвертированную сумму к общей
            if converted_amount:
                total_amount += float(converted_amount)

        except (KeyError, requests.RequestException) as e:
            print(f"Ошибка при конвертации: {e}")
            continue

    # Возвращаем итоговую сумму в рублях
    return round(total_amount, 2)
