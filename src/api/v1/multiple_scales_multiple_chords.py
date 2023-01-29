from scamp import Session
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from typing import Optional
import random

from play_functions.simul_scale_chord import play_multiple_scales_chords
from . import remove_file, convert_midi_file

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


def play_multiple_scales_multiple_chords(tempos: tuple, measures: list, move_scale_max: int, repeat_n_times: int, timeout: int, notes_range: tuple) -> str:

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]

    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    instrument_back = sess.new_part('piano')

    instruments = instrument_solo, instrument_back

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    sess.start_transcribing()

    play_multiple_scales_chords(
        sess, instruments, measures, move_scale_max, repeat_n_times, timeout, notes_range)

    sess.stop_transcribing().save_midi_file(output_file_path, playback_tempo, midi_tempo)

    return output_file_path


@router.post("/multiple_scales_multiple_chords")
def func(fields: RequestFields, background_tasks: BackgroundTasks):

    measures = [(4, scales.all['aeolian'], 'a', chords.all['minor'], None),
                (4, scales.all['ionian'], 'c', chords.all['major'], None)]

    notes_range = (40, 81)

    tempos = (fields.playback_tempo, fields.midi_tempo)

    output_file_path = play_multiple_scales_multiple_chords(
        tempos, measures, fields.move_scale_max, fields.repeat_n_times, None, notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')
