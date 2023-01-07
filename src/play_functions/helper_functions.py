import random
from typing import Tuple, Optional
import time


from entities.move_scale import MoveScale

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


def get_tonation(tonation: str) -> str:
    """if tone_key value is random, randomly pick from all keys list"""

    if tonation not in ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b','random']:
        raise ValueError('Not invalid tone key!')
    elif tonation == 'random':
        return random.choice(list(tone_start.keys()))
    else:
        return tonation
    

def create_tonal_scale_and_primes_lists(scale: list, scale_tonation: str, notes_range: tuple) -> Tuple[list, list]:
    """return list of tonal scale with all notes and also primes pitches"""
    min_notes_range = notes_range[0]
    max_notes_range = notes_range[1]
    primes = list(range(tone_start[scale_tonation],max_notes_range+1,12))
    all_tones = [prime + tone for tone in scale for prime in primes]
    all_tones = [x for x in all_tones if x <= max_notes_range and x >= min_notes_range]
    
    return sorted(all_tones), sorted(primes)


def find_random_notes(quarternotes: int, scale: list, scale_tonation: str,  notes_range: tuple, note_pitch: int, shift_note_index: Optional[int],
                        move_scale_max: int, difficulty: str) -> Tuple[list, int]:

    
    # this object is initialized per every measue so it the whole method needs one less parameter
    move_scale_obj = MoveScale(move_scale_max, difficulty=difficulty)

    tonal_scale, primes = create_tonal_scale_and_primes_lists(
        scale, scale_tonation, notes_range)

    if note_pitch == None:
        # random first note from primes
        note_pitch = random.choice(primes)
    elif note_pitch not in tonal_scale:
        # most similar pitch to previous note pitch
        note_pitch = min(tonal_scale, key=lambda x: abs(x-note_pitch))

    list_of_notes = []

    for _ in range(quarternotes):

        # find new note pitch and what kind of shift was it
        note_pitch, shift_note_index = move_scale_obj.find_new_note(
            shift_note_index, tonal_scale, note_pitch)

        list_of_notes.append(note_pitch)

    # return shift_note_index in order to know what was the last shift of the note
    return list_of_notes, shift_note_index


def get_current_time() -> float:

    time_start = time.time()

    return time_start