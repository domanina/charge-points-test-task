import random
import string
import uuid


def generate_random_string(length: int = 20) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_uuid4() -> str:
    return str(uuid.uuid4())


def is_valid_uuid4(original_string: str) -> bool:
    try:
        val = uuid.UUID(original_string, version=4)
        return val.hex == original_string.replace('-', '')
    except ValueError:
        return False
