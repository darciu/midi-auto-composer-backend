from typing import List, Optional
import random
from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel, Field
import random

from play_functions.simul_scale_chord import play_multiple_scales_chords
from play_functions.helper_functions import get_tonation
from . import remove_file, convert_midi_file

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords

scales = Scales.load()
chords = Chords.load()
scales_chords = ScalesChords.load()

router = APIRouter()


class RequestFields(BaseModel):
    playback_tempo: int = 3500
    midi_tempo: int = 120
    scales: List[str] = ['pentatonic_minor','pentatonic_major']
    scale_tonation: str = 'random'
    chord: str = 'major'
    quarternotes: int = 4
    move_scale_max: int = 2
    repeat_n_times: int = 40
    timeout: Optional[int]
    notes_range: tuple = (40, 81)


def play_random_scales_one_chord(tempos: tuple, scales: List[list], scale_tonation: str, chord: list, chord_tonation: Optional[str], quarternotes: int, move_scale_max: int, repeat_n_times: int, timeout: Optional[int], notes_range: tuple):

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]

    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('Cello')

    instrument_back = sess.new_part('Jazz Guitar')

    instruments = instrument_solo, instrument_back

    scale_tonation = get_tonation(scale_tonation)

    if chord_tonation == None:
        chord_tonation = scale_tonation
    

    measures = []
    for _ in range(repeat_n_times):
        scale = random.choice(scales)
        measures.append(tuple([quarternotes, scale, scale_tonation, chord, chord_tonation]))

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    sess.start_transcribing()

    play_multiple_scales_chords(sess, instruments, measures, move_scale_max, repeat_n_times, timeout, notes_range)

    sess.stop_transcribing().save_midi_file(output_file_path, playback_tempo, midi_tempo)

    return output_file_path


@router.post("/random_scales_one_chord")
def func(fields: RequestFields, background_tasks: BackgroundTasks):

    tempos = (fields.playback_tempo, fields.midi_tempo)

    scales_list = []

    for scale in fields.scales:
        scales_list.append(scales.all[scale])

    chord = chords.all[fields.chord]

    output_file_path = play_random_scales_one_chord(tempos, scales_list, fields.scale_tonation, chord, None, fields.quarternotes, fields.move_scale_max, fields.repeat_n_times, fields.timeout, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')


