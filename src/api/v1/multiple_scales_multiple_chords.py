from scamp import Session
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import pickle
from play_functions.simul_scale_chord import play_multiple_scales_chords

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
    # measures: list
    move_scale_max: int = 2
    repeat_n_times: int = 5
    timeout: Optional[int] = None
    notes_range: tuple = (40, 81)


def play_multiple_scales_multiple_chords(tempos: tuple, measures: list, move_scale_max: int, repeat_n_times: int, timeout: int, notes_range: tuple):

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]

    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    instrument_back = sess.new_part('piano')

    instruments = instrument_solo, instrument_back

    sess.start_transcribing()

    play_multiple_scales_chords(
        sess, instruments, measures, move_scale_max, repeat_n_times, timeout, notes_range)

    midi_obj = sess.stop_transcribing().get_midi_object(playback_tempo, midi_tempo)

    return midi_obj


@router.post("/multiple_scales_multiple_chords")
def func(fields: RequestFields):

    measures = [(4, scales.all['aeolian'], 'a', chords.all['minor'], None),
                (4, scales.all['ionian'], 'c', chords.all['major'], None)]

    notes_range = (40, 81)

    tempos = (fields.playback_tempo, fields.midi_tempo)

    midi_obj = play_multiple_scales_multiple_chords(
        tempos, measures, fields.move_scale_max, fields.repeat_n_times, None, notes_range)

    str_midi_obj = str(pickle.dumps(midi_obj, 0))

    return str_midi_obj
