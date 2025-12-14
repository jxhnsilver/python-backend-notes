from typing import List

def matrix_multiply(a: List[int], b: List[int], n: int) -> List[int]:
    """
    Умножение двух матриц n x n, представленных как одномерные списки.
    Возвращает результат в том же формате.
    """
    if len(a) != n * n or len(b) != n * n:
        raise ValueError("Массивы должны быть размером n x n")

    result = []
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += a[n * i + k] * b[n * k + j]
            result.append(total)
    return result