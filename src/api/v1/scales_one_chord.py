from typing import List, Optional
import random
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
import random

from . import remove_file, convert_midi_file
from .schemas import RequestFieldsScalesOneChord

from entities.midi_composer import MIDIComposer

router = APIRouter()


def compose_scales_one_chord(tempo: int, scales_names: List[str], chord_name: str, tonation: str, quarternotes: int,
                                    difficulty: str, bassline: bool, percussion: bool,
                                    random_sequence: bool, notes_range: tuple):
    
    if difficulty == 'easy':
        move_scale_max = 1
    elif difficulty == 'normal':
        move_scale_max = 2
    elif difficulty == 'hard':
        move_scale_max = 3

    midi_composer = MIDIComposer(tempo, notes_range, move_scale_max, difficulty)

    tonation = midi_composer.get_tonation(tonation)

    # timeout in seconds
    timeout = 100

    melody_volume = 0.8
    background_chords_volume = 0.7
    bassline_volume = 0.8
    percussion_volume = 0.5

    melody_program = 42
    background_chords_program = 2
    bassline_program = 33

    repeat_n_times = midi_composer.timeout_to_n_repeats(timeout, quarternotes*2)

    quarternotes_measures = []
    scales_input = []
    chords_input = []
    
    if random_sequence:
        for _ in range(repeat_n_times):
            scales_input.append((random.choice(scales_names),tonation))
            chords_input.append((chord_name,tonation))
            quarternotes_measures.append(quarternotes)
    else:
        for i in range(repeat_n_times):
            scales_input.append((scales_names[i%len(scales_names)],tonation))
            chords_input.append((chord_name,tonation))
            quarternotes_measures.append(quarternotes)

    midi_composer.add_random_melody_part(scales_input, quarternotes_measures, melody_program, melody_volume)

    midi_composer.add_background_chords_part(chords_input, quarternotes_measures, background_chords_program, background_chords_volume)

    if bassline:
        midi_composer.add_bassline_part(chords_input, quarternotes_measures, bassline_program, bassline_volume)

    if percussion:
        midi_composer.add_percussion_part(quarternotes_measures, percussion_volume)
    

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    return output_file_path, timeout


@router.post("/scales_one_chord", tags=['play_modes'])
def scales_one_chord(fields: RequestFieldsScalesOneChord, background_tasks: BackgroundTasks):
    """One constant chord while playing given scales"""

    output_file_path, time_duration = compose_scales_one_chord(fields.tempo, fields.scales_names, fields.chord_name,
                                                               fields.tonation, fields.quarternotes, fields.difficulty,
                                                               fields.bassline, fields.percussion, fields.random_sequence,
                                                               fields.notes_range)

    convert_midi_file(output_file_path, time_duration, '28000')

    output_file_path = output_file_path.replace('.mid','.mp3')

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.mp3')


