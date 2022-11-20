from scamp import Session
import random
import numpy as np
from typing import Tuple

from src.entities.scales import Scales
from src.entities.move_scale import MoveScale
from src.play_functions.random_notes import play_random_notes

scales = Scales.load_scales()
min_notes_range = 40
max_notes_range = 81

quarternotes = 20

s = Session(tempo=120)
instrument = s.new_part('guitar')


tone_start = {
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

move_scale_max = 2

move_scale_obj = MoveScale(move_scale_max)

def get_tone_key(tone_key: str) -> str:
    """if tone_key value is random, randomly pick from all keys list"""
    if tone_key not in ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b','random']:
        raise ValueError('Not invalid tone key!')
    if tone_key == 'random':
        return random.choice(list(tone_start.keys()))

def create_tonal_scale_and_primes_lists(tone_key: str, scale: list) -> Tuple[list, list]:
    """return list of tonal scale with all notes and also primes"""
    primes = list(range(tone_start[tone_key],max_notes_range+1,12))
    all_tones = [prime + tone for tone in scale for prime in primes]
    all_tones = [x for x in all_tones if x <= max_notes_range and x >= min_notes_range]
    return sorted(all_tones), sorted(primes)






tone_key = get_tone_key('random')

tonal_scale, primes = create_tonal_scale_and_primes_lists(tone_key, scales.all['ionian'])


move_scale_obj.move_scale_board
# random first note (prime)
note_pitch = random.choice(primes)

shift_note_index = None

for _ in range(20):
    note_pitch, shift_note_index = play_random_notes(instrument, 3, tonal_scale, note_pitch, shift_note_index, move_scale_obj)



#na podstawie tempo i metrum oraz timeout ustalane jest ile taktów zostanie granych
