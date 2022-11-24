import random
from typing import Tuple

tone_start: dict = {
        'c':48,
        'c#':49,
        'd':50,
        'd#':51,
        'e':40,
        'f':41,
        'f#':42,
        'g':43,
        'g#':44,
        'a':45,
        'a#':46,
        'b':47,
    }


def get_tone_key(tone_key: str) -> str:
    """if tone_key value is random, randomly pick from all keys list"""

    if tone_key not in ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b','random']:
        raise ValueError('Not invalid tone key!')
    else:
        return tone_key
    if tone_key == 'random':
        return random.choice(list(tone_start.keys()))

def create_tonal_scale_and_primes_lists(tone_key: str, scale: list, min_notes_range: int, max_notes_range: int) -> Tuple[list, list]:
    """return list of tonal scale with all notes and also primes"""
    primes = list(range(tone_start[tone_key],max_notes_range+1,12))
    all_tones = [prime + tone for tone in scale for prime in primes]
    all_tones = [x for x in all_tones if x <= max_notes_range and x >= min_notes_range]
    return sorted(all_tones), sorted(primes)