from typing import List, Tuple, Optional
import random
from scamp import Session
from fastapi import APIRouter
from pydantic import BaseModel
import pickle

from play_functions.background_chords import play_background_chord
from play_functions.helper_functions import get_current_time

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords

scales = Scales.load_scales()
chords = Chords.load_chords()
scales_chords = ScalesChords.create_object()

router = APIRouter()


class RequestFields(BaseModel):
    playback_tempo: int = 3500
    midi_tempo: int = 120
    chords: List[Tuple[str, str]] = [('major', 'c'), ('dominant7', 'f')]
    quarternotes: int = 4
    repeat_n_times: int = 5
    timeout: Optional[int] = None
    notes_range: tuple = (40, 81)


def play_random_background_chords(tempos: tuple, chords: List[Tuple[list, str]], quarternotes: int, repeat_n_times: int, timeout: Optional[int], notes_range: tuple):

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]

    sess = Session(tempo=playback_tempo)

    instrument_back = sess.new_part('piano')

    sess.start_transcribing()

    if timeout == None:

        for _ in range(repeat_n_times):

            chord = random.choice(chords)
            chord_sequence = chord[0]
            chord_tonation = chord[1]

            play_background_chord(
                instrument_back, quarternotes, chord_sequence, chord_tonation, notes_range)

    else:
        start_time = get_current_time()
        current_time = start_time
        while current_time - start_time <= timeout:

            chord = random.choice(chords)
            chord_sequence = chord[0]
            chord_tonation = chord[1]

            play_background_chord(
                instrument_back, quarternotes, chord_sequence, chord_tonation, notes_range)
            current_time = get_current_time()
            
    midi_obj = sess.stop_transcribing().get_midi_object(playback_tempo, midi_tempo)

    return midi_obj

@router.post("/random_background_chords")
def func(fields: RequestFields):

    tempos = (fields.playback_tempo, fields.midi_tempo)

    chords_list = []
    for chord_name, chord_tonation in fields.chords:
        chords_list.append((chords.all[chord_name], chord_tonation))

    midi_obj = play_random_background_chords(
        tempos, chords_list, fields.quarternotes, fields.repeat_n_times, fields.timeout, fields.notes_range)

    str_midi_obj = str(pickle.dumps(midi_obj, 0))

    return str_midi_obj
