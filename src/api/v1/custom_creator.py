import random
from typing import List

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from . import remove_file, convert_midi_file
from .schemas import RequestFieldsCustomCreator
from entities.midi_composer import MIDIComposer

router = APIRouter()


def play_multiple_scales_multiple_chords(tempo: int, components: List[dict], difficulty: str, repeat_n_times: int, bassline: bool, percussion: bool, notes_range: tuple) -> str:


    if difficulty == 'easy':
        move_scale_max = 1
    elif difficulty == 'normal':
        move_scale_max = 2
    elif difficulty == 'hard':
        move_scale_max = 3

    melody_volume = 0.8
    background_chords_volume = 0.7
    bassline_volume = 0.8
    percussion_volume = 0.5

    melody_program = 42
    background_chords_program = 2
    bassline_program = 33

    midi_composer = MIDIComposer(tempo, notes_range, move_scale_max, difficulty)
    
    quarternotes_measures = []
    scales_input = []
    chords_input = []

    for _ in range(repeat_n_times):
        for component in sorted(components, key=lambda d: d['order']):
            tonation = component['tonation']
            quarternotes = component['quarternotes']
            scale_name = component['scale_name']
            chord_name = component['chord_name']

            quarternotes_measures.append(quarternotes)
            scales_input.append((scale_name, tonation,))
            chords_input.append((chord_name, tonation,))


    midi_composer.add_random_melody_part(scales_input, quarternotes_measures, melody_program, melody_volume)

    midi_composer.add_background_chords_part(chords_input, quarternotes_measures, background_chords_program, background_chords_volume)

    if bassline:
        midi_composer.add_bassline_part(chords_input, quarternotes_measures, bassline_program, bassline_volume)

    if percussion:
        midi_composer.add_percussion_part(quarternotes_measures, percussion_volume)

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    return output_file_path, midi_composer.get_time_duration()


@router.post("/custom_creator", tags=['play_modes'])
def custom_creator(fields: RequestFieldsCustomCreator, background_tasks: BackgroundTasks):
    """Providing measures play different scales with different chords in loop"""

    output_file_path, time_duration = play_multiple_scales_multiple_chords(fields.tempo, fields.components, 
                                                            fields.difficulty, fields.repeat_n_times,
                                                            fields.bassline, fields.percussion, fields.notes_range)

    convert_midi_file(output_file_path, time_duration)

    output_file_path = output_file_path.replace('.mid','.mp3')

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.mp3')


