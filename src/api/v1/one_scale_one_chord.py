from typing import Optional
import random

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from . import remove_file, convert_midi_file
from .schemas import RequestFieldsOneScaleOneChord
from entities.midi_composer import MIDIComposer

router = APIRouter()


def play_one_scale_one_chord(tempo: int, scale_name: list, chord_name: list, tonation: str,
                            quarternotes: int, move_scale_max: int, difficulty: str, bassline: bool, percussion: bool,
                            notes_range: tuple) -> str:

    midi_composer = MIDIComposer(tempo, quarternotes, notes_range, move_scale_max, difficulty)

    tonation = midi_composer.get_tonation(tonation)

    # timeout in seconds
    timeout = 60
    repeat_n_times = midi_composer.timeout_to_n_repeats(timeout)

    scales_input = []
    chords_input = []
    for _ in range(repeat_n_times):
        scales_input.append((scale_name,tonation))
        chords_input.append((chord_name,tonation))


    midi_composer.add_random_melody_part(scales_input,25)

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
                            fields.quarternotes, fields.move_scale_max, fields.difficulty, fields.bassline, fields.percussion,
                            fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path.replace('.mid','.mp3'), media_type='application/octet-stream', filename='record.mp3')