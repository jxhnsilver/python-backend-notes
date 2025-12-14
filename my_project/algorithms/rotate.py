



def rotate(array: list[int], k: int) -> list[int]:
    k = k % len(array)
    return array[-k:] + array[:-k]
