from pathlib import Path

import pytest

from src.decorators import log


# Подготовка тестовых функций
@log()
def function_success(x: int, y: int) -> int:
    return x + y


@log()
def function_error(x: int, y: int) -> float:
    if x < 0:
        raise ValueError("Negative value")
    return x / y


# Тесты на успешное выполнение
def test_success_console(capsys: pytest.CaptureFixture) -> None:
    result = function_success(2, 3)
    captured = capsys.readouterr()
    assert result == 5
    assert "Start execution function_success" in captured.out
    assert "function_success ok, result = 5" in captured.out


# Тесты на обработку ошибок с выводом в консоль
def test_error_console(capsys: pytest.CaptureFixture) -> None:
    with pytest.raises(ValueError):
        function_error(-1, 2)
    captured = capsys.readouterr()
    assert "function_error error: Negative value" in captured.out
    assert "Inputs: (-1, 2), {}" in captured.out


# Тесты на обработку ошибок с выводом в файл
def test_error_file(tmp_path: Path) -> None:
    log_file = tmp_path / "test.log"

    @log(str(log_file))
    def func_test(x: int, y: int) -> float:
        if x < 0:
            raise ValueError("Negative value")
        return x / y

    with pytest.raises(ValueError):
        func_test(-1, 2)
    with open(log_file) as file:
        content = file.read()
    assert "func_test error: Negative value" in content
    assert "Inputs: (-1, 2), {}" in content
