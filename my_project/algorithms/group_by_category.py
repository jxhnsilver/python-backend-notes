def group_by_category(items: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result = {}
    for item in items:
        category = item["category"]
        if category not in result:
            result[category] = [item]
        else:
            result[category].append(item)
    return result
