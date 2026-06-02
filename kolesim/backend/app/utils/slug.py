import re
import unicodedata


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).strip().lower()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^\w\-]+", "", value, flags=re.UNICODE)
    return value.strip("-")
