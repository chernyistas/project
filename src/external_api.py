import os

import requests
from dotenv import load_dotenv

# Загрузка переменных из .env-файла
load_dotenv()

API_KEY = os.getenv("API_KEY")


def transaction_amount(transactions: list[dict]) -> float:
    """Функция конвертации валюты из USD и EUR в рубли."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == "RUB":
            print(transaction["operationAmount"]["amount"])
        if transaction["operationAmount"]["currency"]["code"] != "RUB":
            try:
                my_amount = transaction["operationAmount"]["amount"]
                my_from = transaction["operationAmount"]["currency"]["code"]
                my_to = "RUB"
                url = (
                    f"https://api.apilayer.com/exchangerates_data/convert?to={my_to}&from={my_from}&amount={my_amount}"
                )

                headers = {"apikey": API_KEY}

                response = requests.request("GET", url, headers=headers)

                print(response.json())
            except KeyError:
                continue
