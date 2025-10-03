from unittest.mock import Mock, mock_open, patch

from src.external_api import transaction_amount
from src.utils import load_transactions


# Функция-тест для успешного чтения файла
@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]')
def test_load_transactions_success(mock_file: Mock, mock_exists: Mock) -> None:
    result = load_transactions("test.json")
    assert result == [{"id": 1, "amount": 100}], "Должен вернуть список транзакций"
    mock_exists.assert_called_once_with("test.json")
    mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")


# Тест проверки отсутствия файла
def test_file_not_exists() -> None:
    # Создаем mock для os.path.exists
    with patch("os.path.exists") as mock_exists:
        # Задаем возвращаемое значение для проверки существования файла
        mock_exists.return_value = False

        # Вызываем тестируемую функцию
        result = load_transactions("non_existent_file.json")

        # Проверяем, что результат пустой список
        assert result == []
        # Проверяем, что os.path.exists был вызван с правильным путем
        mock_exists.assert_called_once_with("non_existent_file.json")


def test_mixed_elements() -> None:
    # Проверяем случай со смешанными типами данных
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True

        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = [
                {"id": 1, "amount": 100},  # Корректный словарь
                "не словарь",  # Некорректный элемент
                {"id": 2, "amount": 200},  # Корректный словарь
                42,  # Некорректный элемент
            ]

            result = load_transactions("mixed_file.json")
            assert result == [], "Ошибка при проверке смешанных типов данных"


def test_json_decode_error_with_empty_file() -> None:
    # Создаем mock для проверки существования файла
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True

        # Создаем mock для открытия пустого файла
        with patch("builtins.open", mock_open(read_data="")):
            # Вызываем тестируемую функцию
            result = load_transactions("empty_file.json")

            # Проверяем, что результат - пустой список
            assert result == [], "Ожидался пустой список при ошибке декодирования"

            # Проверяем вызовы моков
            mock_exists.assert_called_once_with("empty_file.json")


# Тест 1: конвертация USD в RUB
def test_usd_conversion(transactions_usd: list) -> None:
    with patch("requests.get") as mock_get:
        # Мокаем ответ API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 9500.0}  # пример курса 95 руб за доллар
        mock_get.return_value = mock_response

        result = transaction_amount(transactions_usd)
        assert result == 9500.00, "Неверный результат конвертации USD"


# Тест 2: конвертация EUR в RUB
def test_eur_conversion(transactions_eur: list) -> None:
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 6000.0}  # пример курса 120 руб за евро
        mock_get.return_value = mock_response

        result = transaction_amount(transactions_eur)
        assert result == 6000.00, "Неверный результат конвертации EUR"


# Тест 3: рубли без конвертации
def test_rub_conversion(transactions_rub: list) -> None:
    with patch("requests.get") as mock_get:
        # API не должен вызываться для рублей
        mock_get.return_value = None

        result = transaction_amount(transactions_rub)
        assert result == 2000.00, "Ошибка при обработке рублей"


# Дополнительный тест для пустого списка транзакций
def test_empty_transactions() -> None:
    result = transaction_amount([])
    assert result == 0.00, "При пустом списке транзакций должно быть 0.00, " f"получено {result}"
