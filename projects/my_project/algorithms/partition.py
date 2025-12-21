



def partition(array:list[int]) -> tuple[list[int], list[int]]:
    evens: list[int] = []
    odds: list[int] = []

    for item in array:
        if item % 2 == 0:
            evens.append(item)
        else:
            odds.append(item)

    return evens, odds