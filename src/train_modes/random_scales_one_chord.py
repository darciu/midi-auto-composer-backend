from typing import Optional, List
import random

from scamp import Session

from play_functions.simul_scale_chord import play_multiple_scales_chords
from play_functions.helper_functions import get_tonation


def play_random_scales_one_chord(playback_tempo: int, scales: List[list], scale_tonation: str, chord: list, chord_tonation: Optional[str], quarternotes: int, move_scale_max: int, repeat_n_times: int, timeout: Optional[int],notes_range: tuple):


    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    instrument_back = sess.new_part('piano')

    instruments = instrument_solo, instrument_back

    scale_tonation = get_tonation(scale_tonation)

    if chord_tonation == None:
        chord_tonation = scale_tonation
    
    if timeout != None:
        repeat_n_times = 999

    measures = []
    for _ in range(repeat_n_times):

        scale = random.choice(scales)
        measures.append(tuple([quarternotes, scale, scale_tonation, chord, chord_tonation]))

    play_multiple_scales_chords(sess, instruments, measures, move_scale_max, 1, timeout, notes_range)

