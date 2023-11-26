from typing import List, Optional
import random
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
import random

from . import remove_file, convert_midi_file
from .schemas import RequestFieldsRandomScalesOneChord

from entities.midi_composer import MIDIComposer

router = APIRouter()


def compose_random_scales_one_chord(tempo: int, scales: List[str], chord_name: str, tonation: str, quarternotes: int,
                                    move_scale_max: int, difficulty: str, bassline: bool, percussion: bool, notes_range: tuple):

    

    midi_composer = MIDIComposer(tempo, notes_range, move_scale_max, difficulty)

    tonation = midi_composer.get_tonation(tonation)

    # timeout in seconds
    timeout = 60
    repeat_n_times = midi_composer.timeout_to_n_repeats(timeout, quarternotes)

    quarternotes_measures = []
    scales_input = []
    chords_input = []
    for _ in range(repeat_n_times):
        scales_input.append((random.choice(scales),tonation))
        chords_input.append((chord_name,tonation))
        quarternotes_measures.append(quarternotes)

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


@router.post("/random_scales_one_chord", tags=['play_modes'])
def random_scales_one_chord(fields: RequestFieldsRandomScalesOneChord, background_tasks: BackgroundTasks):
    """One constant chord while playing given scales"""

    output_file_path = compose_random_scales_one_chord(fields.tempo, fields.scales, fields.chord_name, fields.tonation,
                                                       fields.quarternotes, fields.move_scale_max, fields.difficulty, fields.bassline,
                                                       fields.percussion, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path.replace('.mid','.mp3'), media_type='application/octet-stream', filename='record.mp3')


