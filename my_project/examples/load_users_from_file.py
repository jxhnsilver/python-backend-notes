from typing import List, Dict
import os


def load_users_from_file(filename: str) -> List[Dict[str, str]]:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл {filename} не найден.")

    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return []

    headers = lines[0].split(',')
    users = []
    for line in lines[1:]:
        values = line.split(',')
        if len(values) != len(headers):
            continue  # пропускаем некорректные строки
        user = dict(zip(headers, values))
        users.append(user)

    return users


if __name__ == "__main__":
    file_name = "test.txt"
    users = load_users_from_file(file_name)
