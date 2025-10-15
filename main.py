import os

from src.df_reader import df_csv_transactions, read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.transactions_utils import process_bank_search
from src.utils import load_transactions
from src.widget import get_date, mask_account_card

json_path = os.path.join(os.getcwd(), "data", "operations.json")
csv_path = os.path.join(os.getcwd(), "data", "transactions.csv")
xlsx_path = os.path.join(os.getcwd(), "data", "transactions_excel.xlsx")


def main() -> None:
    """Функция, которая отвечает за основную логику проекта и связывает функциональности между собой."""
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор формата файла
    file_format = input()

    if file_format == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        transactions = load_transactions(json_path)
    elif file_format == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        transactions = df_csv_transactions(csv_path)
    elif file_format == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        transactions = read_transactions_from_excel(xlsx_path)
    else:
        print("Программа: Неверный формат файла. Завершение работы.")
        return

    # Фильтрация по статусу
    valid_states = ["EXECUTED", "CANCELED", "PENDING"]
    state = ""
    while state not in valid_states:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтрации статусы:", ", ".join(valid_states))
        state = input().strip().upper()

        if state not in valid_states:
            print(f"Программа: Статус операции '{state}' недоступен.")

    filtered_transactions = filter_by_state(transactions, state)
    print(f"Программа: Операции отфильтрованы по статусу '{state}'")

    # Сортировка по дате
    sort_date = input("Программа: Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_date in ["да", "yes"]:
        sort_order = input("Программа: Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        filtered_transactions = sort_by_date(
            filtered_transactions, ascending=(sort_order in ["по возрастанию", "ascending"])
        )
    # Фильтрация по валюте
    rub_filter = input("Программа: Выводить только рублевые транзакции? Да/Нет\n").strip().lower()

    if rub_filter in ["да", "yes"]:
        filtered_transactions = [
            tx
            for tx in filtered_transactions
            if tx.get("currency_code") == "RUB"
            or tx.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]
    # Фильтрация по слову в описании
    word_filter = (
        input("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
    )
    if word_filter in ["да", "yes"]:
        search_word = input("Программа: Введите слово для поиска:\n").strip().lower()
        filtered_transactions = process_bank_search(filtered_transactions, search_word)

    # Вывод результата

    print("Программа: Распечатываю итоговый список транзакций...")
    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа: Всего банковских операций в выборке: {len(filtered_transactions)}")

    for tx in filtered_transactions:
        currency = tx.get("currency_name") or tx.get("operationAmount", {}).get("currency", {}).get("name")
        formatted_date = get_date(tx.get("date"))
        from_account = tx.get("from")
        if from_account:
            from_account = mask_account_card(from_account)
        else:
            # Обработка случая, когда from пустой
            print("Отсутствует информация об отправителе.")

        to_account = mask_account_card(tx.get("to"))
        description = tx.get("description")
        amount = tx.get("amount") or tx.get("operationAmount", {}).get("amount")
        if description == "Открытие вклада":
            print(f"{formatted_date} {description}\n{to_account}\nСумма: {amount} руб.\n")
        elif "Перевод с карты на карту" in description:
            print(f"{formatted_date} {description}\n{from_account} -> {to_account}\nСумма: {amount} {currency}\n")
        elif "Перевод организации" in description:
            print(f"{formatted_date} {description}\n{from_account} -> {to_account}\nСумма: {amount} {currency}\n")
        elif "Перевод со счета на счет" in description:
            print(f"{formatted_date} {description}\n{from_account} -> {to_account}\nСумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
