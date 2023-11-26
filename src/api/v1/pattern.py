from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
import random

from . import remove_file, convert_midi_file
from entities.midi_composer import MIDIComposer

router = APIRouter()

from .schemas import RequestFieldsPattern

def compose_pattern(tempo: int, pattern: list, scale_name: str, tonation: str, play_upwards: bool, preview_pattern: bool, pause_between: bool, notes_range: tuple) -> str:

    

    midi_composer = MIDIComposer(tempo, notes_range)

    tonation = midi_composer.get_tonation(tonation)

    midi_composer.add_scale_pattern_part(pattern, scale_name, tonation, play_upwards, preview_pattern, pause_between)

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    return output_file_path
    

@router.post("/pattern", tags=['play_modes'])
def pattern(fields: RequestFieldsPattern, background_tasks: BackgroundTasks):
    """Playing pattern on scale basis"""
        
    output_file_path = compose_pattern(fields.tempo, fields.pattern, fields.scale_name, fields.tonation, fields.play_upwards, fields.preview_pattern, fields.pause_between, fields.notes_range)
    
    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path.replace('.mid','.mp3'), media_type='application/octet-stream', filename='record.mp3')



