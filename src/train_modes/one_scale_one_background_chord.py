from typing import Optional
from scamp import Session

# python -m src.play_modes.random_scale_chord_background

from play_functions.scale_preview import play_scale_preview
from play_functions.simul_scale_chord import play_multiple_scales_chords

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords

scales = Scales.load_scales()
chords = Chords.load_chords()
scales_chords = ScalesChords.create_object()



def play_one_scale_one_background_chord(playback_tempo: int, scale: list, scale_tonation: str, chord: list, chord_tonation: Optional[str], quarternotes: int, move_scale_max: int, scale_preview: bool, play_background_chord, repeat_n_times: int, notes_range: tuple):

    if chord_tonation == None:
        chord_tonation = scale_tonation

    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    if play_background_chord and scale != scales.all['chromatic']:
        instrument_back = sess.new_part('piano')
    else:
        instrument_back = None

    instruments = instrument_solo, instrument_back
    
    if scale_preview:
        play_scale_preview(instrument_solo, scale, scale_tonation, notes_range)

    # only one measure
    measures = [(quarternotes, scale, scale_tonation, chord, chord_tonation)]

    play_multiple_scales_chords(sess, instruments, measures, move_scale_max, repeat_n_times, notes_range)


    