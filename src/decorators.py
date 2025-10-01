from functools import wraps
from typing import Callable, Optional, ParamSpec, TypeVar

T = TypeVar("T")  # Обобщённый тип для возвращаемого значения
P = ParamSpec("P")  # Параметры функции, которую декорируем


def log(filename: Optional[str] = None) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Декоратор автоматически логирует начало и конец выполнения функции,
    а также ее результат или возникшие ошибки."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # Определяем куда писать логи
            if filename:
                with open(filename, "a") as file:
                    file.write(f"Start execution {func.__name__}\n")

            else:
                print(f"Start execution {func.__name__}")

            try:
                result = func(*args, **kwargs)
                if filename:
                    with open(filename, "a") as file:
                        file.write(f"{func.__name__} ok, result = {result}")
                else:
                    print(f"{func.__name__} ok, result = {result}")

                return result

            except Exception as e:

                if filename:
                    with open(filename, "a") as file:
                        file.write(f"{func.__name__} error: {str(e)}. Inputs: {args}, {kwargs}")
                else:
                    print(f"{func.__name__} error: {str(e)}. Inputs: {args}, {kwargs}")
                raise

        return wrapper

    return decorator
