from typing import List, Tuple, Optional
import random
from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel, Field
import random

from play_functions.background_chords import play_background_chord
from play_functions.helper_functions import get_current_time
from . import remove_file, convert_midi_file

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords

scales = Scales.load()
chords = Chords.load()
scales_chords = ScalesChords.load()

router = APIRouter()


class RequestFieldsBackgroundChords(BaseModel):
    playback_tempo: int = Field(default=3500)
    midi_tempo: int = Field(default=120, title='Recording file tempo')
    chords: List[Tuple[str, str]] = Field(default=[('major', 'c'), ('dominant7', 'f')], title='Chords to play')
    quarternotes: int = Field(default= 4, title='How many quarternotes per measure')
    repeat_n_times: int = Field(default= 20, title='How many repetitions of measure')
    timeout: Optional[int] = Field(default=None, title='Optional timeout', nullable=True)
    notes_range: tuple = Field(default=(40, 81), title='Scales pitch range')

    class Config:
        schema_extra = {
            "example": {
                "playback_tempo": 3500,
                "midi_tempo": 120,
                "chords": [('major', 'c'), ('dominant7', 'f')],
                "quarternotes": 4,
                "repeat_n_times": 20,
                "notes_range": (40, 81)
            }
        }


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
def random_background_chords(fields: RequestFieldsBackgroundChords, background_tasks: BackgroundTasks):
    """Play chords randomly"""

    tempos = (fields.playback_tempo, fields.midi_tempo)

    chords_list = []
    for chord_name, chord_tonation in fields.chords:
        chords_list.append((chords.all[chord_name], chord_tonation))

    output_file_path = play_random_background_chords(
        tempos, chords_list, fields.quarternotes, fields.repeat_n_times, fields.timeout, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')
