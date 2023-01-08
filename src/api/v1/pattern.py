from scamp import Session
from fastapi import APIRouter
from pydantic import BaseModel
import pickle

from play_functions.scale_with_pattern import play_scale_with_pattern_upwards, play_scale_with_pattern_downwards

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
    scale: str = 'mixolydian'
    scale_tonation: str = 'a'
    pattern: list = [1,2,3]
    play_upwards: bool = True
    notes_range: tuple = (40, 81)

def play_pattern(tempos: tuple, scale: list, scale_tonation: str, pattern: list, play_upwards: bool, notes_range: tuple):

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]

    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    sess.start_transcribing()

    if play_upwards:

        play_scale_with_pattern_upwards(instrument_solo, scale, scale_tonation, pattern, notes_range)

    else:

        play_scale_with_pattern_downwards(instrument_solo, scale, scale_tonation, pattern, notes_range)

    midi_obj = sess.stop_transcribing().get_midi_object(playback_tempo, midi_tempo)

    return midi_obj

@router.post("/pattern")
def func(fields: RequestFields):

    tempos = (fields.playback_tempo, fields.midi_tempo)

    scale = scales.all[fields.scale]
    
    midi_obj = play_pattern(tempos, scale, fields.scale_tonation, fields.pattern, fields.play_upwards, fields.notes_range)

    str_midi_obj = str(pickle.dumps(midi_obj, 0))

    return str_midi_obj