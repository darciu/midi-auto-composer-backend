import random

from scamp import Session, wait
import scamp

# python -m src.play_modes.scale_with_pattern

from ..entities.move_scale import MoveScale
from ..entities.scales import Scales
from ..entities.chords import Chords
from ..entities.scales_chords import ScalesChords
from ..play_functions.helper_functions import (
    create_tonal_scale_and_primes_lists, get_tone_key)
from ..play_functions.random_scale_notes import play_list_of_notes, find_random_notes
from ..play_functions.background_chords import play_background_chord

scales = Scales.load_scales()
chords = Chords.load_chords()
scales_chords = ScalesChords.create_object()

min_notes_range = 40
max_notes_range = 81

s = Session(tempo=100)
instrument = s.new_part('guitar')

tone_key = 'a'

scale = scales.all['ionian']
print(scale)

pattern=[3,1]

upwards = True

tone_key = get_tone_key(tone_key)

tonal_scale, _ = create_tonal_scale_and_primes_lists(tone_key,scale,min_notes_range,max_notes_range)

# dodać break w notacji
def present_pattern(instrument, pattern, tonal_scale):


    for i in range(len(pattern)):
 
        instrument.play_note(tonal_scale[pattern[i]-1],1,1)


if upwards:
    present_pattern(instrument, pattern, tonal_scale)

    wait(3)
    for step in tonal_scale:

        if not tonal_scale.index(step) + max(pattern) >= len(tonal_scale) + 1:
            for pattern_step in pattern:

                note_index = tonal_scale.index(step) + pattern_step -1
                instrument.play_note(tonal_scale[note_index], 1, 1)
            wait(1)
    instrument.play_note(tonal_scale[-1],1,1)

else:
    tonal_scale_reversed = list(reversed(tonal_scale))
    present_pattern(instrument, pattern, tonal_scale)
    
    wait(3)
    for step in tonal_scale_reversed:
        if not tonal_scale_reversed.index(step) + max(pattern) -1 >= len(tonal_scale_reversed):
            for pattern_step in pattern:
                note_index = tonal_scale_reversed.index(step) + pattern_step -1
                instrument.play_note(tonal_scale_reversed[note_index],1,1)
            wait(1)
    instrument.play_note(tonal_scale_reversed[-1],1,1)