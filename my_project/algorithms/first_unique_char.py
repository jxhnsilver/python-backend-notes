def first_unique_char(s: str) -> str:
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    for char in freq:
        if freq[char] == 1:
            return char
    return str()
