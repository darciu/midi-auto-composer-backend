from typing import Optional
from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel
import random

from play_functions.scale_preview import play_scale_preview
from play_functions.simul_scale_chord import play_multiple_scales_chords
from play_functions.helper_functions import get_tonation
from . import remove_file

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
    chord: str = 'major'
    chord_tonation: Optional[str] = 'a'
    quarternotes: int = 4
    move_scale_max: int = 2
    scale_preview: bool = True
    play_background_chord: bool = True
    repeat_n_times: int = 4
    timeout: Optional[int] = None
    notes_range: tuple = (40, 81)


def play_one_scale_one_chord(tempos: tuple, scale: list, scale_tonation: str, chord: list, chord_tonation: Optional[str],
                            quarternotes: int, move_scale_max: int, scale_preview: bool, play_background_chord: bool, repeat_n_times: int,
                            timeout: Optional[int], notes_range: tuple) -> str:

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]


    sess = Session(tempo = playback_tempo)

    instrument_solo = sess.new_part('cello')

    if play_background_chord and scale != scales.all['chromatic']:
        instrument_back = sess.new_part('piano')
    else:
        instrument_back = None

    instruments = instrument_solo, instrument_back
    

    scale_tonation = get_tonation(scale_tonation)

    if chord_tonation == None:
        chord_tonation = scale_tonation

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    sess.start_transcribing()
    
    if scale_preview:
        play_scale_preview(instrument_solo, scale, scale_tonation, notes_range)

    # only one measure
    measures = [(quarternotes, scale, scale_tonation, chord, chord_tonation)]

    play_multiple_scales_chords(sess, instruments, measures, move_scale_max, repeat_n_times, timeout, notes_range)

    sess.stop_transcribing().save_midi_file(output_file_path, playback_tempo, midi_tempo)

    return output_file_path


@router.post("/one_scale_one_chord")
def func(fields: RequestFields, background_tasks: BackgroundTasks):

    tempos = (fields.playback_tempo, fields.midi_tempo)

    scale = scales.all[fields.scale]
    chord = chords.all[fields.chord]
    

    output_file_path = play_one_scale_one_chord(tempos, scale, fields.scale_tonation, chord, fields.chord_tonation,
                            fields.quarternotes, fields.move_scale_max, fields.scale_preview, fields.play_background_chord, fields.repeat_n_times,
                            fields.timeout, fields.notes_range)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.mid')