import random

from scamp import Session
import scamp

# python -m src.play_modes.random_scale_chord_background

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



# params:
min_notes_range = 40
max_notes_range = 81

s = Session(tempo=110)



instrument = s.new_part('Cello')
instrument_back = s.new_part('Honky-tonk Piano')

quarternotes = 4

move_scale_max = 3


measures = [(4, scales.all['pentatonic_minor'], chords.chords['minor'],
             'b'), (4, scales.all['pentatonic_major'], chords.chords['major'], 'g')]

measures = [(4, scales.all['pentatonic_minor'], chords.chords['dominant7'],
             'g'), (4, scales.all['pentatonic_major'], chords.chords['major'], 'g')]


def multiple_scale_chord(instrument: scamp.instruments.ScampInstrument, instrument_back: scamp.instruments.ScampInstrument, measures: list, move_scale_max: int, repeat_n_times: int, min_notes_range: int, max_notes_range: int):

    note_pitch = None
    for _ in range(repeat_n_times):

        for measure in measures:
            note_pitch = single_scale_chord(
                instrument, instrument_back, measure[0], measure[1], measure[2], measure[3], note_pitch, move_scale_max, min_notes_range, max_notes_range)


def single_scale_chord(instrument: scamp.instruments.ScampInstrument, instrument_back: scamp.instruments.ScampInstrument, quarternotes: 4, scale: list, chord: list, tonation: str, note_pitch: int, move_scale_max: int, min_notes_range: int, max_notes_range: int):

    move_scale_obj = MoveScale(move_scale_max, difficulty='hard')

    tone_key = get_tone_key(tonation)

    tonal_scale, primes = create_tonal_scale_and_primes_lists(
        tone_key, scale, min_notes_range, max_notes_range)

    tonal_chord, _ = create_tonal_scale_and_primes_lists(
        tone_key, chord, min_notes_range, max_notes_range)

    shift_note_index = None

    if note_pitch == None:
        # random first note (prime)
        note_pitch = random.choice(primes)

    elif note_pitch not in tonal_scale:
        note_pitch = min(tonal_scale, key=lambda x: abs(x-note_pitch))

    list_of_notes, shift_note_index = find_random_notes(
        quarternotes, tonal_scale, note_pitch, shift_note_index, move_scale_obj)
    note_pitch = list_of_notes[-1]
    s.fork(play_list_of_notes, args=[instrument, list_of_notes])
    s.fork(play_background_chord, args=[
           instrument_back, quarternotes, tonal_chord,0.4])
    s.wait_for_children_to_finish()

    return note_pitch


multiple_scale_chord(instrument, instrument_back, measures,
                     move_scale_max, 10, min_notes_range, max_notes_range)

