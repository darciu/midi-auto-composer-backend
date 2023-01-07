from scamp import  wait
from scamp.instruments import ScampInstrument


from play_functions.helper_functions import (
    create_tonal_scale_and_primes_lists, get_tonation)


def present_pattern(instrument_solo: ScampInstrument, tonal_scale: list, pattern: list):

    for i in range(len(pattern)):
 
        instrument_solo.play_note(tonal_scale[pattern[i]-1],1,0.5)


def play_scale_with_pattern_upwards(instrument_solo: ScampInstrument, scale: list, scale_tonation: str, pattern: list, notes_range: tuple) -> None:


    scale_tonation = get_tonation(scale_tonation)

    tonal_scale, _ = create_tonal_scale_and_primes_lists(scale, scale_tonation, notes_range)

    present_pattern(instrument_solo, tonal_scale, pattern)

    wait(3)
    for scale_step in tonal_scale:

        if not tonal_scale.index(scale_step) + max(pattern) >= len(tonal_scale) + 1:
            for pattern_step in pattern:

                note_index = tonal_scale.index(scale_step) + pattern_step -1
                instrument_solo.play_note(tonal_scale[note_index], 1, 1)
            wait(1)
    instrument_solo.play_note(tonal_scale[-1],1,1)



def play_scale_with_pattern_downwards(instrument_solo: ScampInstrument, scale: list, scale_tonation: str, pattern: list, notes_range: tuple) -> None:


    scale_tonation = get_tonation(scale_tonation)

    tonal_scale, _ = create_tonal_scale_and_primes_lists(scale, scale_tonation, notes_range)


    tonal_scale_reversed = list(reversed(tonal_scale))


    present_pattern(instrument_solo, tonal_scale_reversed, pattern)
    
    wait(3)
    for scale_step in tonal_scale_reversed:
        if not tonal_scale_reversed.index(scale_step) + max(pattern) -1 >= len(tonal_scale_reversed):
            for pattern_step in pattern:
                note_index = tonal_scale_reversed.index(scale_step) + pattern_step -1
                instrument_solo.play_note(tonal_scale_reversed[note_index],1,1)
            wait(1)
    instrument_solo.play_note(tonal_scale_reversed[-1],1,1)

