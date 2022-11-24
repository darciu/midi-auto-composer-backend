import random

from scamp import Session



from ..entities.move_scale import MoveScale
from ..entities.scales import Scales
from ..entities.chords import Chords
from ..entities.scales_chords import ScalesChords
from ..play_functions.helper_functions import (
    create_tonal_scale_and_primes_lists, get_tone_key)
from ..play_functions.random_scale_notes import play_list_of_notes, random_notes
from ..play_functions.background_chords import play_background_chords

scales = Scales.load_scales()
chords = Chords.load_chords()
scales_chords = ScalesChords.create_object()


# params:
min_notes_range = 40
max_notes_range = 81

s = Session(tempo=140)
instrument = s.new_part('guitar')
instrument_back = s.new_part('piano')

quarternotes = 4

move_scale_max = 2







def play_scale_chord(instrument, instrument_back, quarternotes, scale, chord, tonation, note_pitch, move_scale_max, min_notes_range, max_notes_range):

    move_scale_obj = MoveScale(move_scale_max)

    tone_key = get_tone_key(tonation)

    tonal_scale, primes = create_tonal_scale_and_primes_lists(tone_key, scale, min_notes_range, max_notes_range)

    tonal_chord, _ = create_tonal_scale_and_primes_lists(tone_key, chord, min_notes_range, max_notes_range)
    if note_pitch == None:
        # random first note (prime)
        note_pitch = random.choice(primes)
    elif note_pitch not in tonal_scale:
        note_pitch = min(tonal_scale, key=lambda x:abs(x-note_pitch))

    shift_note_index = None

    list_of_notes, shift_note_index = random_notes(quarternotes, tonal_scale, note_pitch, shift_note_index, move_scale_obj)
    note_pitch = list_of_notes[-1]
    s.fork(play_list_of_notes, args=[instrument, list_of_notes])
    s.fork(play_background_chords, args=[instrument_back, quarternotes, tonal_chord])
    s.wait_for_children_to_finish()

    return note_pitch



for _ in range(3):
    note_pitch = play_scale_chord(instrument, instrument_back, quarternotes, scales.all['ionian'], chords.chords['major'], 'a', None, move_scale_max, min_notes_range, max_notes_range)

    note_pitch= play_scale_chord(instrument, instrument_back, quarternotes, scales.all['lydian'], chords.chords['maj7'], 'c', note_pitch ,move_scale_max, min_notes_range, max_notes_range)

    note_pitch= play_scale_chord(instrument, instrument_back, quarternotes, scales.all['ionian'], chords.chords['major'], 'a',note_pitch, move_scale_max, min_notes_range, max_notes_range)

    note_pitch = play_scale_chord(instrument, instrument_back, quarternotes, scales.all['mixolydian'], chords.chords['dominant7'], 'e',note_pitch, move_scale_max, min_notes_range, max_notes_range)

    note_pitch = play_scale_chord(instrument, instrument_back, quarternotes, scales.all['mixolydian'], chords.chords['dominant7'], 'f',note_pitch, move_scale_max, min_notes_range, max_notes_range)