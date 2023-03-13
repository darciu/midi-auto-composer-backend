from typing import List, Optional, Literal
import random
from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel, Field
from enum import Enum
import random

from play_functions.simul_scale_chord import play_multiple_scales_chords
from play_functions.helper_functions import get_tonation
from . import remove_file, convert_midi_file

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords
from entities.midi_composer import MIDIComposer

scales = Scales.load()
chords = Chords.load()
scales_chords = ScalesChords.load()

class Difficulty(str, Enum):
    ionian = "easy"
    harmonic_minor = "normal"
    melodic_minor = "hard"


router = APIRouter()


class RequestFieldsRandomScalesOneChord(BaseModel):
    tempo: int = Field(default=120, title='Recording file tempo')
    scales: List[str] = Field(default=['pentatonic_minor','pentatonic_major'], title='Scales to play')
    tonation: str = Field(default='random', title='Tonation')
    chord_name: str = Field(default='major', title='Background chord name')
    quarternotes: int = Field(default= 4, title='How many quarternotes per measure')
    move_scale_max: int = Field(default= 2, title='Maximum movement through the scale steps')
    difficulty: Difficulty = Field(default='normal', title='Higher level of difficulty means that random melody notes will have greate intervals')
    bassline: bool = Field(default=True, title='Add bassine to the recording')
    percussion: bool = Field(default=True, title='Add percusion beat to the recording')
    repeat_n_times: int = Field(default= 40, title='How many repetitions of measure')
    timeout: Optional[int] = Field(default=None, title='Optional timeout', nullable=True)
    notes_range: tuple = Field(default=(40, 81), title='Scales pitch range')

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "scales": ['pentatonic_minor','pentatonic_major'],
                "tonation": "random",
                "chord_name":"major",
                "quarternotes": 4,
                "move_scale_max": 2,
                "difficulty": "normal",
                "bassline": True,
                "percussion": True,
                "repeat_n_times": 40,
                "notes_range": (40, 81)
            }
        }


def play_random_scales_one_chord(tempo: int, scales: List[str], chord_name: str, tonation: str, quarternotes: int, move_scale_max: int, difficulty: str, bassline: bool, percussion: bool, repeat_n_times: int, timeout: Optional[int], notes_range: tuple):

    tonation = get_tonation(tonation)

    midi_composer = MIDIComposer(tempo, quarternotes, notes_range, move_scale_max, difficulty)


    scales_input = []
    chords_input = []
    for _ in range(repeat_n_times):
        scales_input.append((random.choice(scales),tonation))
        chords_input.append((chord_name,tonation))

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


@router.post("/random_scales_one_chord", tags=['play_modes'])
def random_scales_one_chord(fields: RequestFieldsRandomScalesOneChord, background_tasks: BackgroundTasks):
    """One constant chord while playing given scales"""

    output_file_path = play_random_scales_one_chord(fields.tempo, fields.scales, fields.chord_name, fields.tonation, fields.quarternotes, fields.move_scale_max, fields.difficulty, fields.bassline, fields.percussion, fields.repeat_n_times, fields.timeout, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')


