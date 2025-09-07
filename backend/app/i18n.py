from typing import Dict

MESSAGES: Dict[str, Dict[str, str]] = {
    "en": {
        "greeting": "Hello from API"
    },
    "ru": {
        "greeting": "Привет из API"
    },
}


def get_message(key: str, lang: str) -> str:
    """Return a localized message by key and language code."""
    lang_code = lang.split("-")[0]
    return MESSAGES.get(lang_code, MESSAGES["en"]).get(key, key)
