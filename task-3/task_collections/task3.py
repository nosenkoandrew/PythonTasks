from collections import Counter
from functools import lru_cache


@lru_cache
def non_repeating_elems(text):
    if not isinstance(text, str):
        raise TypeError(f'Passed variable should be text, got {type(text)}')

    return sum(value for value in Counter(text).values() if value == 1)

