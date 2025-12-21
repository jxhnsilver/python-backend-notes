from typing import Protocol

class Notifier(Protocol):
    """Абстракция для отправки уведомлений — DIP в чистом виде."""
    def send(self, message: str) -> None: ...


class UserService:
    """
    Зависит от абстракции Notifier, а не от конкретной реализации.
    Это и есть Dependency Inversion Principle (DIP).
    """
    def __init__(self, notifier: Notifier):
        self._notifier = notifier

    def register(self, name: str) -> None:
        self._notifier.send(f"Добро пожаловать, {name}!")


# Конкретные реализации (могут быть в других модулях)
class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[EMAIL] {message}")


class SmsNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[SMS] {message}")


# Пример использования
if __name__ == "__main__":
    user_service1 = UserService(EmailNotifier())
    user_service1.register("Иван")

    user_service2 = UserService(SmsNotifier())
    user_service2.register("София")