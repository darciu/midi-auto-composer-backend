from scamp import Session
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from typing import Optional, List, Tuple
import random

from play_functions.simul_scale_chord import play_multiple_scales_chords
from . import remove_file, convert_midi_file

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords

scales = Scales.load()
chords = Chords.load()
scales_chords = ScalesChords.load()

router = APIRouter()

class RequestFieldsMultipleScalesMultipleChords(BaseModel):
    playback_tempo: int = Field(default=3500)
    midi_tempo: int = Field(default=120, title='Recording file tempo')
    measures: List[Tuple[int,list,str,list,Optional[str]]] = Field(default=[(4, scales.all['aeolian'], 'a', chords.all['minor'], None),
                                  (4, scales.all['ionian'], 'c', chords.all['major'], None)], title='Measures as tuple of: quarternotes, scale, scale tonation, chord, optional chord tonation')
    move_scale_max: int = Field(default= 2, title='Maximum movement through the scale steps')
    repeat_n_times: int = Field(default= 40, title='How many repetitions of measure')
    timeout: Optional[int] = Field(default=None, title='Optional timeout', nullable=True)
    notes_range: tuple = Field(default=(40, 81), title='Scales pitch range')

    class Config:
        schema_extra = {
            "example": {
                "playback_tempo": 3500,
                "midi_tempo": 120,
                "measures": [(4, scales.all['aeolian'], 'a', chords.all['minor'], None),(4, scales.all['ionian'], 'c', chords.all['major'], None)],
                "move_scale_max": 2,
                "repeat_n_times": 40,
                "notes_range": (40, 81)
            }
        }



def play_multiple_scales_multiple_chords(tempos: tuple, measures: list, move_scale_max: int, repeat_n_times: int, timeout: int, notes_range: tuple) -> str:

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]

    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    instrument_back = sess.new_part('piano')

    instruments = instrument_solo, instrument_back

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    sess.start_transcribing()

    play_multiple_scales_chords(
        sess, instruments, measures, move_scale_max, repeat_n_times, timeout, notes_range)

    sess.stop_transcribing().save_midi_file(output_file_path, playback_tempo, midi_tempo)

    return output_file_path


@router.post("/multiple_scales_multiple_chords", tags=['play_modes'])
def multiple_scales_multiple_chords(fields: RequestFieldsMultipleScalesMultipleChords, background_tasks: BackgroundTasks):
    """Providing measures play different scales with different chords in loop"""

    notes_range = (40, 81)

    tempos = (fields.playback_tempo, fields.midi_tempo)

    output_file_path = play_multiple_scales_multiple_chords(
        tempos, fields.measures, fields.move_scale_max, fields.repeat_n_times, fields.timeout, notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')
