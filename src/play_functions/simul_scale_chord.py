import random

from scamp import Session
from scamp.instruments import ScampInstrument

from ..entities.move_scale import MoveScale
from helper_functions import get_tone_key, create_tonal_scale_and_primes_lists, find_random_notes
from background_chords import play_background_chord
from list_of_notes import play_list_of_notes

def play_multiple_scale_chord(sess: Session, instrument: ScampInstrument, instrument_backing: ScampInstrument, measures: list, 
                        move_scale_max: int, repeat_n_times: int, min_notes_range: int, max_notes_range: int):

    note_pitch = None
    for _ in range(repeat_n_times):

        for measure in measures:
            note_pitch = play_single_scale_chord(sess,
                instrument, instrument_backing, measure[0], measure[1], measure[2], measure[3], 
                note_pitch, move_scale_max, min_notes_range, max_notes_range)





def play_single_scale_chord(sess: Session, instrument: ScampInstrument, instrument_back: ScampInstrument, quarternotes: 4, 
                    scale: list, chord: list, tonation: str, note_pitch: int, move_scale_max: int, min_notes_range: int, max_notes_range: int):

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
    sess.fork(play_list_of_notes, args=[instrument, list_of_notes])
    sess.fork(play_background_chord, args=[
           instrument_back, quarternotes, tonal_chord,0.3])
    sess.wait_for_children_to_finish()

    return note_pitch