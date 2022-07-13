def is_in_string(string: str, words: tuple) -> bool:
    for word in words:
        if word in string:
            return True
    return False
