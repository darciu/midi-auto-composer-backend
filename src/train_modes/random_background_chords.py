from typing import List, Tuple, Optional
import random

from scamp import Session

from play_functions.background_chords import play_background_chord
from play_functions.helper_functions import get_current_time


def play_random_background_chords(playback_tempo: int, chords: List[Tuple[list,str]], quarternotes: int, repeat_n_times: int, timeout: Optional[int], notes_range: tuple):

    sess = Session(tempo=playback_tempo)

    instrument_back = sess.new_part('piano')
    
    if timeout == None:

        for _ in range(repeat_n_times):

            chord = random.choice(chords)
            chord_sequence = chord[0]
            chord_tonation = chord[1]
            
            play_background_chord(instrument_back, quarternotes, chord_sequence, chord_tonation, notes_range)

    else:
        start_time = get_current_time()
        current_time = start_time
        while current_time - start_time <= timeout:

            chord = random.choice(chords)
            chord_sequence = chord[0]
            chord_tonation = chord[1]
            
            play_background_chord(instrument_back, quarternotes, chord_sequence, chord_tonation, notes_range)
            current_time = get_current_time()



    

