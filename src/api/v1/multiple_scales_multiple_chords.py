from fastapi import APIRouter
from pydantic import BaseModel, Field
from enum import Enum
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from typing import Optional, List, Tuple
import random

from play_functions.simul_scale_chord import play_multiple_scales_chords
from . import remove_file, convert_midi_file

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords
from entities.midi_composer import MIDIComposer

scales = Scales.load()
chords = Chords.load()
scales_chords = ScalesChords.load()

router = APIRouter()

class Difficulty(str, Enum):
    ionian = "easy"
    harmonic_minor = "normal"
    melodic_minor = "hard"

class RequestFieldsMultipleScalesMultipleChords(BaseModel):
    tempo: int = Field(default=120, title='Recording file tempo')
    scales = Field(default=[('ionian','d'),('dorian','e')], title='List of tuples: scale - tonation to be played')
    chords = Field(default=[('major','d'),('minor','e')], title='List of tuples: chord - tonation to be played')
    quarternotes: int = Field(default= 4, title='How many quarternotes per measure')
    move_scale_max: int = Field(default= 2, title='Maximum movement through the scale steps')
    difficulty: Difficulty = Field(default='normal', title='Higher level of difficulty means that random melody notes will have greate intervals')
    bassline: bool = Field(default=True, title='Add bassine to the recording')
    percussion: bool = Field(default=True, title='Add percusion beat to the recording')
    repeat_n_times: int = Field(default= 20, title='How many repetitions of measure')
    timeout: Optional[int] = Field(default=None, title='Optional timeout', nullable=True)
    notes_range: tuple = Field(default=(40, 81), title='Scales pitch range')

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "scales": [('ionian','d'),('dorian','e')],
                "chords": [('major','d'),('minor','e')],
                "move_scale_max": 2,
                "difficulty": "normal",
                "bassline": True,
                "percussion": True,
                "repeat_n_times": 20,
                "notes_range": (40, 81)
            }
        }



def play_multiple_scales_multiple_chords(tempo: int, quarternotes: int,  scales: list, chords: str, move_scale_max: int, difficulty: str, bassline: bool, percussion: bool, repeat_n_times: int, timeout: int, notes_range: tuple) -> str:

    if len(scales) == len(chords):
        sequence_len = len(scales)
    else:
        raise ValueError('Scales and chords are not equal')

    midi_composer = MIDIComposer(tempo, quarternotes, notes_range, move_scale_max, difficulty)

    if timeout:
        repeat_n_times = midi_composer.timeout_to_n_repeats(timeout, sequence_len)

    scales_input = scales*repeat_n_times

    chords_input = chords*repeat_n_times

    # odpowiednia walidacja

    midi_composer.add_random_melody_part(scales_input,42)

    midi_composer.add_background_chords_part(chords_input, 2)

    if bassline:
        midi_composer.add_bassline_part(chords_input, 33)

    if percussion:
        midi_composer.add_percussion_part(repeat_n_times*sequence_len)

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    

    return output_file_path


@router.post("/multiple_scales_multiple_chords", tags=['play_modes'])
def multiple_scales_multiple_chords(fields: RequestFieldsMultipleScalesMultipleChords, background_tasks: BackgroundTasks):
    """Providing measures play different scales with different chords in loop"""


    output_file_path = play_multiple_scales_multiple_chords(fields.tempo, fields.quarternotes, fields.scales, fields.chords, fields.move_scale_max, fields.difficulty, fields.bassline, fields.percussion, fields.repeat_n_times, fields.timeout, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')
