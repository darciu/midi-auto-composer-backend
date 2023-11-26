import random

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from . import remove_file, convert_midi_file
from .schemas import RequestFieldsCustomCreator
from entities.midi_composer import MIDIComposer

router = APIRouter()


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


@router.post("/custom_creator", tags=['play_modes'])
def multiple_scales_multiple_chords(fields: RequestFieldsCustomCreator, background_tasks: BackgroundTasks):
    """Providing measures play different scales with different chords in loop"""




    output_file_path = play_multiple_scales_multiple_chords(fields.tempo, fields.quarternotes, 
                                                            fields.scales, fields.chords, 
                                                            fields.move_scale_max, fields.difficulty, 
                                                            fields.bassline, fields.percussion, 
                                                            fields.repeat_n_times, fields.timeout, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')
