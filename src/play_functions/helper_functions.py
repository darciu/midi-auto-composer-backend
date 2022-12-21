import random
from typing import Tuple, Optional


from ..entities.move_scale import MoveScale

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
    elif tone_key == 'random':
        return random.choice(list(tone_start.keys()))
    else:
        return tone_key
    

def create_tonal_scale_and_primes_lists(tone_key: str, scale: list, min_notes_range: int, max_notes_range: int) -> Tuple[list, list]:
    """return list of tonal scale with all notes and also primes pitches"""
    primes = list(range(tone_start[tone_key],max_notes_range+1,12))
    all_tones = [prime + tone for tone in scale for prime in primes]
    all_tones = [x for x in all_tones if x <= max_notes_range and x >= min_notes_range]
    return sorted(all_tones), sorted(primes)





def find_random_notes(quarternotes: int, tonal_scale: list, note_pitch: int, shift_note_index: Optional[int],
                        move_scale_obj: MoveScale) -> Tuple[list, int]:

    list_of_notes = []

    for _ in range(quarternotes):

        note_pitch, shift_note_index = move_scale_obj.find_new_note(
            shift_note_index, tonal_scale, note_pitch)

        list_of_notes.append(note_pitch)

    return list_of_notes, shift_note_index