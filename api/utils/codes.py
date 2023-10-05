import random
from string import ascii_letters, digits


def generate_code(characters: str, length: int) -> str:
    """
    Generates a code of the specified length using
    the provided characters.
    """
    code = [random.choice(characters) for _ in range(length)]
    return "".join(code)


def generate_digits_code(length: int) -> str:
    """
    Generates a code from digits of the specified
    length.
    """
    return generate_code(digits, length)


def generate_alpha_code(length: int) -> str:
    """
    Generates a code from letters of the specified
    length.
    """
    return generate_code(ascii_letters, length)
