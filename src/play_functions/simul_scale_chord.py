from typing import Tuple

from scamp import Session
from scamp.instruments import ScampInstrument


from play_functions.helper_functions import find_random_notes
from play_functions.background_chords import play_background_chord
from play_functions.list_of_notes import play_list_of_notes

def play_multiple_scales_chords(sess: Session, instruments: Tuple[ScampInstrument, ScampInstrument], measures: list, 
                        move_scale_max: int, repeat_n_times: int, notes_range: tuple):


    prev_note_pitch = None
    for _ in range(repeat_n_times):

        for measure in measures:
            prev_note_pitch = play_single_scale_chord_measure(sess, instruments, measure,  prev_note_pitch, move_scale_max, notes_range)



def play_single_scale_chord_measure(sess: Session, instruments: Tuple[ScampInstrument, ScampInstrument], measure: list, prev_note_pitch: int, move_scale_max: int, notes_range: tuple, difficulty: str = 'normal') -> int:
    
    # this means that probability of nex move is distrubuted as default
    shift_note_index = None

    instrument_solo = instruments[0]
    instrument_back = instruments[1]

    quarternotes = measure[0]
    scale = measure[1]
    scale_tonation = measure[2]
    chord = measure[3]
    chord_tonation = measure[4]
    

    # this part finds list of random notes
    list_of_notes, shift_note_index = find_random_notes(
        quarternotes, scale, scale_tonation, notes_range, prev_note_pitch, shift_note_index, move_scale_max, difficulty)
    last_note_pitch = list_of_notes[-1]
    if instrument_back != None:
    
        sess.fork(play_list_of_notes, args=[instrument_solo, list_of_notes])
        sess.fork(play_background_chord, args=[
            instrument_back, quarternotes, chord, chord_tonation, notes_range ,0.3])
        sess.wait_for_children_to_finish()

    else:
        sess.fork(play_list_of_notes, args=[instrument_solo, list_of_notes])
        sess.wait_for_children_to_finish()
        
    return last_note_pitch