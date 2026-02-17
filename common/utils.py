import re
import uuid


def is_english_only(s: str) -> str:
    return bool(re.fullmatch(r'[A-Za-z-]+', s))


def get_hex_id():
    return uuid.uuid4().hex
