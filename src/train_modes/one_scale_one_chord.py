from typing import Optional
from scamp import Session


from play_functions.scale_preview import play_scale_preview
from play_functions.simul_scale_chord import play_multiple_scales_chords
from play_functions.helper_functions import get_tonation

from entities.scales import Scales

scales = Scales.load_scales()


def play_one_scale_one_chord(playback_tempo: int, scale: list, scale_tonation: str, chord: list, chord_tonation: Optional[str],
                            quarternotes: int, move_scale_max: int, scale_preview: bool, play_background_chord, repeat_n_times: int,
                            timeout: Optional[int], notes_range: tuple):


    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    if play_background_chord and scale != scales.all['chromatic']:
        instrument_back = sess.new_part('piano')
    else:
        instrument_back = None

    instruments = instrument_solo, instrument_back

    scale_tonation = get_tonation(scale_tonation)

    if chord_tonation == None:
        chord_tonation = scale_tonation
    
    if scale_preview:
        play_scale_preview(instrument_solo, scale, scale_tonation, notes_range)

    # only one measure
    measures = [(quarternotes, scale, scale_tonation, chord, chord_tonation)]

    play_multiple_scales_chords(sess, instruments, measures, move_scale_max, repeat_n_times, timeout, notes_range)