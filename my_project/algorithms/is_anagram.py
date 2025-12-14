def is_anagram(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    f1, f2 = {}, {}

    for c in s1:
        c = c.lower()

        f1[c] = f1.get(c, 0) + 1
    for c in s2:
        c = c.lower()
        f2[c] = f2.get(c, 0) + 1
    return f1 == f2
