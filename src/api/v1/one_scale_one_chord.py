from typing import Optional
from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel, Field
from enum import Enum
import random

from play_functions.scale_preview import play_scale_preview
from play_functions.simul_scale_chord import play_multiple_scales_chords
from play_functions.helper_functions import get_tonation
from . import remove_file, convert_midi_file

from entities.midi_composer import MIDIComposer


router = APIRouter()

class Difficulty(str, Enum):
    ionian = "easy"
    harmonic_minor = "normal"
    melodic_minor = "hard"

class RequestFieldsOneScaleOneChord(BaseModel):
    tempo: int = Field(default=120, title='Recording file tempo')
    scale_name: str = Field(default='mixolydian', title='Scale to be played')
    chord_name: str = Field(default='major', title='Background chord')
    tonation: str = Field(default='random', title='Tonation')
    quarternotes: int = Field(default= 4, title='How many quarternotes per measure')
    move_scale_max: int = Field(default= 2, title='Maximum movement through the scale steps')
    difficulty: Difficulty = Field(default='normal', title='Higher level of difficulty means that random melody notes will have greate intervals')
    bassline: bool = Field(default=True, title='Add bassline to the recording')
    percussion: bool = Field(default=True, title='Add percusion beat to the recording')
    scale_preview: bool = Field(default=True, title='Whether to play scale preview at the beginning')
    repeat_n_times: int = Field(default= 40, title='How many repetitions of measure')
    timeout: Optional[int] = Field(default=None, title='Optional timeout', nullable=True)
    notes_range: tuple = Field(default=(40, 81), title='Scales pitch range')

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "scale_name": 'mixolydian',
                "chord_name":"major",
                "tonation": "random",
                "quarternotes": 4,
                "move_scale_max": 2,
                "difficulty": "normal",
                "bassline": True,
                "percussion": True,
                "scale_preview": True,
                "repeat_n_times": 40,
                "notes_range": (40, 81)
            }
        }


def play_one_scale_one_chord(tempo: int, scale_name: list, chord_name: list, tonation: str,
                            quarternotes: int, move_scale_max: int, difficulty: str, bassline: bool, percussion: bool, scale_preview: bool, repeat_n_times: int,
                            timeout: Optional[int], notes_range: tuple) -> str:

    

    tonation = get_tonation(tonation)


    midi_composer = MIDIComposer(tempo, quarternotes, notes_range, move_scale_max, difficulty)

    if timeout:
        repeat_n_times = midi_composer.timeout_to_n_repeats(timeout)

    scales_input = []
    chords_input = []
    for _ in range(repeat_n_times):
        scales_input.append((scale_name,tonation))
        chords_input.append((chord_name,tonation))

    # if play_scale_preview:
    #     midi_composer.add_scale_pattern_part(pattern, scale_name, tonation, play_upwards, preview_pattern, pause_between)

    midi_composer.add_random_melody_part(scales_input,42)

    midi_composer.add_background_chords_part(chords_input, 2)

    if bassline:
        midi_composer.add_bassline_part(chords_input, 33)

    if percussion:
        midi_composer.add_percussion_part(repeat_n_times)
    

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    return output_file_path


@router.post("/one_scale_one_chord", tags=['play_modes'])
def one_scale_one_chord(fields: RequestFieldsOneScaleOneChord, background_tasks: BackgroundTasks):
    """Play constant scale with a chord"""
    

    output_file_path = play_one_scale_one_chord(fields.tempo, fields.scale_name, fields.chord_name, fields.tonation,
                            fields.quarternotes, fields.move_scale_max, fields.difficulty, fields.bassline, fields.percussion, fields.scale_preview, fields.repeat_n_times,
                            fields.timeout, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')