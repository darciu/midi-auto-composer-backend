from typing import List, Optional

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
import random

from . import remove_file, convert_midi_file
from .schemas import RequestFieldsIntervals

from entities.midi_composer import MIDIComposer

router = APIRouter()

def compose_intervals(tempo: int, intervals: List[str], difficulty: str, notes_range: tuple):

    timeout = 100

    midi_composer = MIDIComposer(tempo, notes_range, difficulty=difficulty)

    midi_composer.add_intervals_melody_part(intervals, 1, timeout)

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    return output_file_path, timeout


@router.post("/intervals", tags=['play_modes'])
def intervals(fields: RequestFieldsIntervals, background_tasks: BackgroundTasks):
    """Play random selected intervals"""

    output_file_path, time_duration = compose_intervals(fields.tempo, fields.intervals, fields.difficulty, fields.notes_range)

    convert_midi_file(output_file_path, time_duration + 2, '22050')

    output_file_path = output_file_path.replace('.mid','.mp3')

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.mp3')