import secrets
import string


def generate_token(length: int) -> str:
    alphabet = rf"{string.digits}{string.ascii_letters}{string.punctuation}"
    return r"".join(secrets.choice(alphabet) for _ in range(length))
