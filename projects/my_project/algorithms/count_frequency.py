def count_frequency(items: list[int]) -> dict[int, int]:
    result = {}
    for item in items:
        if item in result:
            result[item] += 1
        else:
            result[item] = 1
    return result
