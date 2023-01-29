from typing import List, Tuple, Optional
import random
from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel
import random

from play_functions.background_chords import play_background_chord
from play_functions.helper_functions import get_current_time
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
    chords: List[Tuple[str, str]] = [('major', 'c'), ('dominant7', 'f')]
    quarternotes: int = 4
    repeat_n_times: int = 5
    timeout: Optional[int] = None
    notes_range: tuple = (40, 81)


def play_random_background_chords(tempos: tuple, chords: List[Tuple[list, str]], quarternotes: int, repeat_n_times: int, timeout: Optional[int], notes_range: tuple) -> str:

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]

    sess = Session(tempo=playback_tempo)

    instrument_back = sess.new_part('piano')

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

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
            
    sess.stop_transcribing().save_midi_file(output_file_path, playback_tempo, midi_tempo)

    return output_file_path

@router.post("/random_background_chords")
def func(fields: RequestFields, background_tasks: BackgroundTasks):

    tempos = (fields.playback_tempo, fields.midi_tempo)

    chords_list = []
    for chord_name, chord_tonation in fields.chords:
        chords_list.append((chords.all[chord_name], chord_tonation))

    output_file_path = play_random_background_chords(
        tempos, chords_list, fields.quarternotes, fields.repeat_n_times, fields.timeout, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')
