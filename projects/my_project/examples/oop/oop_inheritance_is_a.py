from abc import ABC, abstractmethod
from typing import List

class Shape(ABC):
    """
    Абстрактная геометрическая фигура.
    Любая фигура — это Shape (is-a).
    Содержит:
      - общие поля (цвет, название),
      - общую логику (описание),
      - абстрактный контракт (area, render),
      - защищённое состояние.
    """
    def __init__(self, name: str, color: str = "white"):
        self.name = name
        self.color = color
        self._created = True  # общее состояние

    @abstractmethod
    def area(self) -> float:
        """Контракт: каждая фигура должна уметь вычислять площадь."""
        pass

    @abstractmethod
    def render(self) -> str:
        """Контракт: каждая фигура должна уметь себя отображать."""
        pass

    def describe(self) -> str:
        """Общая логика: описание фигуры."""
        return f"{self.name} ({self.color}), площадь: {self.area():.2f}"


class Circle(Shape):
    """Круг — это фигура (is-a)."""
    def __init__(self, radius: float, color: str = "white"):
        super().__init__("Круг", color)
        if radius <= 0:
            raise ValueError("Радиус должен быть положительным")
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def render(self) -> str:
        return f"○ (радиус={self.radius})"

    # Метод, уникальный для Circle
    def diameter(self) -> float:
        return 2 * self.radius


class Rectangle(Shape):
    """Прямоугольник — это фигура (is-a)."""
    def __init__(self, width: float, height: float, color: str = "white"):
        super().__init__("Прямоугольник", color)
        if width <= 0 or height <= 0:
            raise ValueError("Ширина и высота должны быть положительными")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def render(self) -> str:
        return f"▭ ({self.width}×{self.height})"

    # Метод, уникальный для Rectangle
    def is_square(self) -> bool:
        # return self.width == self.height # можно так сделать для упрощенного варианта
        return abs(self.width - self.height) < 0.000000001 # width и height — это float, числа с плавающей точкой хранятся неточно (идёт сравнение длины и ширины с погрешностью)


# Пример использования
if __name__ == "__main__":
    shapes: List[Shape] = [
        Circle(5, "красный"),
        Rectangle(4, 6, "синий"),
        Rectangle(3, 3, "зелёный"),
    ]

    for shape in shapes:
        print(shape.describe())
        print("Отображение:", shape.render())

    # Вызов уникальных методов
    circle = Circle(2)
    print(f"Диаметр круга: {circle.diameter()}")

    rect = Rectangle(5, 5)
    print(f"Это квадрат? {rect.is_square()}")