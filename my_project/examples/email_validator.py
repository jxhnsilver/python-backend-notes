def is_valid_email(email: str) -> bool:
    # 1. Базовая длина и наличие @
    if not email or len(email) > 254 or '@' not in email:
        return False

    # 2. Только один @
    if email.count('@') != 1:
        return False

    local, domain = email.rsplit('@', 1)

    # 3. Проверка длины частей
    if not (1 <= len(local) <= 64) or not (1 <= len(domain) <= 253):
        return False

    # Проверка точки в домене
    if '.' not in domain:
        return False

    return True


if __name__ == "__main__":
    print(is_valid_email("ilya@example.com"))  # True
    print(is_valid_email("user.name+tag@domain.co.uk"))  # True
    print(is_valid_email("bad.email"))  # False
    print(is_valid_email("a@b"))  # False (домен слишком короткий по паттерну)
    print(is_valid_email("user@@domain.com"))  # False