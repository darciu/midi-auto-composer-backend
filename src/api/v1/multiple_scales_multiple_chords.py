from scamp import Session
from fastapi import APIRouter
from pydantic import BaseModel
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
    playback_tempo: int = 120
    # measures: list
    move_scale_max: int = 2
    repeat_n_times: int = 1
    timeout: int = 3
    # notes_range: tuple


    

def play_multiple_scales_multiple_chords(playback_tempo: int, measures: list, move_scale_max: int, repeat_n_times: int, timeout: int, notes_range: tuple):


    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    instrument_back = sess.new_part('piano')

    instruments = instrument_solo, instrument_back

    midi_tempo = playback_tempo

    sess.start_transcribing()

    play_multiple_scales_chords(sess, instruments, measures, move_scale_max, repeat_n_times, timeout, notes_range)

    midi_obj = sess.stop_transcribing().get_midi_object(playback_tempo, midi_tempo)

    return midi_obj



    
@router.post("/play_multiple_scales_multiple_chords")
def func(fields: RequestFields):

    measures = [(4, scales.all['aeolian'], 'a', chords.all['minor'],None)
            ,(4,scales.all['ionian'],'c',chords.all['major'],None)]

    notes_range = (40, 81)


    midi_obj =  play_multiple_scales_multiple_chords(fields.playback_tempo, measures, fields.move_scale_max, fields.repeat_n_times, None, notes_range)

    pickled = str(pickle.dumps(midi_obj, 0))

    return pickled





