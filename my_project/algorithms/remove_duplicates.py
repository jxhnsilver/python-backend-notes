def remove_duplicates(items: list[int]) -> list[int]:
    exists = set()
    result = []
    for item in items:
        if item not in exists:
            exists.add(item)
            result.append(item)
    return result
