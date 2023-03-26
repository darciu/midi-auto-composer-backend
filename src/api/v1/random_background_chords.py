from typing import List, Tuple, Optional
import random
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel, Field
import random

from . import remove_file, convert_midi_file

from entities.midi_composer import MIDIComposer


router = APIRouter()


class RequestFieldsBackgroundChords(BaseModel):
    tempo: int = Field(default=120, title='Recording file tempo')
    chords: List[Tuple[str, str]] = Field(default=[('major', 'c'), ('dominant7', 'f')], title='Chords to play')
    quarternotes: int = Field(default= 4, title='How many quarternotes per measure')
    bassline: bool = Field(default=True, title='Add bassline to the recording')
    percussion: bool = Field(default=True, title='Add percusion beat to the recording')
    repeat_n_times: int = Field(default= 20, title='How many repetitions of measure')
    timeout: Optional[int] = Field(default=None, title='Optional timeout', nullable=True)
    notes_range: tuple = Field(default=(40, 81), title='Scales pitch range')

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "chords": [('major', 'c'), ('dominant7', 'f')],
                "quarternotes": 4,
                "bassline": True,
                "percussion": True,
                "repeat_n_times": 20,
                "notes_range": (40, 81)
            }
        }


def compose_random_background_chords(tempo: int, chords: list, quarternotes: int, bassline: bool, percussion: bool, repeat_n_times: Optional[int], timeout: Optional[int], notes_range: tuple) -> str:


    midi_composer = MIDIComposer(tempo, quarternotes, notes_range)

    if timeout:
        repeat_n_times = midi_composer.timeout_to_n_repeats(timeout)

    chords_input = []
    for _ in range(repeat_n_times):
        chords_input.append(random.choice(chords))

    midi_composer.add_background_chords_part(chords_input, 2)

    if bassline:
        midi_composer.add_bassline_part(chords_input, 33)

    if percussion:
        midi_composer.add_percussion_part(repeat_n_times)
    

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    return output_file_path

@router.post("/random_background_chords", tags=['play_modes'])
def random_background_chords(fields: RequestFieldsBackgroundChords, background_tasks: BackgroundTasks):
    """Play chords randomly"""

    output_file_path = compose_random_background_chords(fields.tempo, fields.chords, fields.quarternotes, fields.bassline, fields.percussion, fields.repeat_n_times, fields.timeout, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')
