import csv
from unittest.mock import mock_open, patch

import pandas as pd

from src.df_reader import df_csv_transactions, read_transactions_from_excel


def test_csv_reader(csv_data: str) -> None:
    # Проверка успешных транзакций

    expected_data = [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": "16210",
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]

    with patch("builtins.open", mock_open(read_data=csv_data)):

        with patch("csv.DictReader") as mock_dict_reader:

            mock_dict_reader.return_value = iter(expected_data)

            result = df_csv_transactions("dummy_path.csv")

            assert len(result) == 1, "Должна быть одна запись"

            assert result == expected_data, "Данные не совпадают"

            record = result[0]
            assert record["id"] == "650703", "Неверный ID"
            assert record["state"] == "EXECUTED", "Неверное состояние"
            assert record["date"] == "2023-09-05T11:30:32Z", "Неверная дата"
            assert record["amount"] == "16210", "Неверная сумма"
            assert record["currency_name"] == "Sol", "Неверное название валюты"
            assert record["currency_code"] == "PEN", "Неверный код валюты"
            assert record["from"] == "Счет 58803664561298323391", "Неверный отправитель"
            assert record["to"] == "Счет 39745660563456619397", "Неверный получатель"
            assert record["description"] == "Перевод организации", "Неверное описание"

            # Проверяем вызовы методов
            mock_dict_reader.assert_called_once()


def test_empty_file() -> None:
    # Проверяем обработку пустого файла
    empty_csv = ""

    with patch("builtins.open", mock_open(read_data=empty_csv)):
        result = df_csv_transactions("empty_file.csv")
        assert result == []


def test_invalid_csv() -> None:
    # Проверяем обработку некорректного CSV
    invalid_csv = "id,date\n1,2025-10-12,100.50,USD,EUR"

    with patch("builtins.open", mock_open(read_data=invalid_csv)):
        try:
            df_csv_transactions("invalid_file.csv")
        except csv.Error as csv_error:
            assert str(csv_error)


def test_read_transactions_success() -> None:
    # Проверка успешных транзакций
    test_data = {"date": ["2023-01-01", "2023-01-02"], "amount": [100.0, 200.0], "description": ["Test1", "Test2"]}
    mock_df = pd.DataFrame(test_data)

    with patch("src.df_reader.pd.read_excel") as mock_read_excel:

        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("test_file.xlsx")

        mock_read_excel.assert_called_once_with("test_file.xlsx", sheet_name=0, header=0, engine="openpyxl")

        assert len(result) == 2
        assert result[0]["date"] == "2023-01-01"
        assert result[1]["amount"] == 200.0
        assert result[0]["description"] == "Test1"


def test_read_transactions_file_not_found() -> None:
    # Проверка если файл не найден
    with patch("src.df_reader.pd.read_excel") as mock_read_excel:

        mock_read_excel.side_effect = FileNotFoundError

        result = read_transactions_from_excel("non_existent_file.xlsx")

        assert result == []


def test_read_transactions_general_error() -> None:
    # Проверка на различные ошибки
    with patch("src.df_reader.pd.read_excel") as mock_read_excel:

        mock_read_excel.side_effect = Exception("Some error")

        result = read_transactions_from_excel("problematic_file.xlsx")

        assert result == []


def test_empty_exel_file() -> None:
    # Проверяем обработку пустого файла
    with patch("src.df_reader.pd.read_excel") as mock_read_excel:

        mock_df = pd.DataFrame()
        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("empty_file.xlsx")

        assert result == []
