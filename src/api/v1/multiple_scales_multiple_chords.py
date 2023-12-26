import random
from typing import List, Tuple, Optional

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from . import remove_file, convert_midi_file
from .schemas import RequestFieldsCustomCreator
from entities.midi_composer import MIDIComposer

router = APIRouter()


def play_multiple_scales_multiple_chords(tempo: int, components: List[Tuple[str,int,Optional[str],str]], move_scale_max: int, difficulty: str, repeat_n_times: int, bassline: bool, percussion: bool, notes_range: tuple) -> str:

    midi_composer = MIDIComposer(tempo, notes_range, move_scale_max, difficulty)
    
    quarternotes_measures = []
    scales_input = []
    chords_input = []

    for _ in range(repeat_n_times):
        for component in components:
            tonation = component[0]
            quarternotes = component[1]
            scale_name = component[2]
            chord_name = component[3]

            quarternotes_measures.append(quarternotes)
            scales_input.append((scale_name, tonation,))
            chords_input.append((chord_name, tonation,))


    midi_composer.add_random_melody_part(scales_input, quarternotes_measures, 25)

    midi_composer.add_background_chords_part(chords_input, quarternotes_measures, 2)

    if bassline:
        midi_composer.add_bassline_part(chords_input, quarternotes_measures, 33)

    if percussion:
        midi_composer.add_percussion_part(quarternotes_measures)

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    return output_file_path


@router.post("/custom_creator", tags=['play_modes'])
def custom_creator(fields: RequestFieldsCustomCreator, background_tasks: BackgroundTasks):
    """Providing measures play different scales with different chords in loop"""

    output_file_path = play_multiple_scales_multiple_chords(fields.tempo, fields.components, 
                                                            fields.move_scale_max, fields.difficulty, fields.repeat_n_times,
                                                            fields.bassline, fields.percussion, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path.replace('.mid','.mp3'), media_type='application/octet-stream', filename='record.mp3')
