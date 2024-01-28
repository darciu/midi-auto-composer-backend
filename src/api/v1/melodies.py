from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
import random

from . import remove_file, convert_midi_file
from .schemas import RequestFieldsMelody

from entities.midi_composer import MIDIComposer

router = APIRouter()

def play_melody(tempo: int, tonation: str, melody_id: str, notes_range: tuple):

    midi_composer = MIDIComposer(tempo, notes_range)

    tonation = midi_composer.get_tonation(tonation)

    midi_composer.add_melody(tonation, melody_id)

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    return output_file_path, midi_composer.get_time_duration()


@router.post("/melody", tags=['play_modes'])
def intervals(fields: RequestFieldsMelody, background_tasks: BackgroundTasks):
    """Play melody"""

    output_file_path, time_duration = play_melody(fields.tempo, fields.tonation, fields.melody_id, fields.notes_range)

    convert_midi_file(output_file_path, time_duration + 2)

    output_file_path = output_file_path.replace('.mid','.mp3')

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.mp3')