import re

from core.data_lists.bad_words_list import INAPPROPRIATE_WORDS


def contains_inappropriate_language(text):
    pattern = r'\b(?:' + '|'.join(map(re.escape, INAPPROPRIATE_WORDS)) + r')\b'
    return re.search(pattern, text, re.IGNORECASE) is not None


def validate_inappropriate_language(data):
    """
    Перевіряє, чи немає у вказаних даних нецензурної лексики.
    Повертає список полів, що містять нецензурну лексику.
    """
    inappropriate_fields = []
    for field, value in data.items():
        if isinstance(value, str) and contains_inappropriate_language(value):
            inappropriate_fields.append(field)
    return inappropriate_fields
