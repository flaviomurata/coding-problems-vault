import random
import string


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_integer(a: int, b: int) -> int:
    return random.randint(a, b)
