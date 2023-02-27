from typing import Optional
from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel, Field
import random

from play_functions.scale_preview import play_scale_preview
from play_functions.simul_scale_chord import play_multiple_scales_chords
from play_functions.helper_functions import get_tonation
from . import remove_file, convert_midi_file

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords

scales = Scales.load()
chords = Chords.load()
scales_chords = ScalesChords.load()


router = APIRouter()


class RequestFieldsOneScaleOneChord(BaseModel):
    playback_tempo: int = Field(default=3500)
    midi_tempo: int = Field(default=120, title='Recording file tempo')
    scale: str = Field(default='mixolydian', title='Scale to be played')
    scale_tonation: str = Field(default='random', title='Scales tonation')
    chord: str = Field(default='major', title='Background chord')
    quarternotes: int = Field(default= 4, title='How many quarternotes per measure')
    move_scale_max: int = Field(default= 2, title='Maximum movement through the scale steps')
    scale_preview: bool = Field(default=True, title='Whether to play scale preview at the beginning')
    play_background_chord: bool = Field(default=True, title='Play a chord in background')
    repeat_n_times: int = Field(default= 40, title='How many repetitions of measure')
    timeout: Optional[int] = Field(default=None, title='Optional timeout', nullable=True)
    notes_range: tuple = Field(default=(40, 81), title='Scales pitch range')

    class Config:
        schema_extra = {
            "example": {
                "playback_tempo": 3500,
                "midi_tempo": 120,
                "scale": 'mixolydian',
                "scale_tonation": "random",
                "chord":"major",
                "quarternotes": 4,
                "move_scale_max": 2,
                "scale_preview": True,
                "play_background_chord": True,
                "repeat_n_times": 40,
                "notes_range": (40, 81)
            }
        }


def play_one_scale_one_chord(tempos: tuple, scale: list, scale_tonation: str, chord: list, chord_tonation: Optional[str],
                            quarternotes: int, move_scale_max: int, scale_preview: bool, play_background_chord: bool, repeat_n_times: int,
                            timeout: Optional[int], notes_range: tuple) -> str:

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]


    sess = Session(tempo = playback_tempo)

    instrument_solo = sess.new_part('cello')

    if play_background_chord and scale != scales.all['chromatic']:
        instrument_back = sess.new_part('piano')
    else:
        instrument_back = None

    instruments = instrument_solo, instrument_back
    

    scale_tonation = get_tonation(scale_tonation)

    if chord_tonation == None:
        chord_tonation = scale_tonation

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    sess.start_transcribing()
    
    if scale_preview:
        play_scale_preview(instrument_solo, scale, scale_tonation, notes_range)

    # only one measure
    measures = [(quarternotes, scale, scale_tonation, chord, chord_tonation)]

    play_multiple_scales_chords(sess, instruments, measures, move_scale_max, repeat_n_times, timeout, notes_range)

    sess.stop_transcribing().save_midi_file(output_file_path, playback_tempo, midi_tempo)

    return output_file_path


@router.post("/one_scale_one_chord", tags=['play_modes'])
def one_scale_one_chord(fields: RequestFieldsOneScaleOneChord, background_tasks: BackgroundTasks):
    """Play constant scale with a chord"""
    
    tempos = (fields.playback_tempo, fields.midi_tempo)

    scale = scales.all[fields.scale]
    chord = chords.all[fields.chord]
    

    output_file_path = play_one_scale_one_chord(tempos, scale, fields.scale_tonation, chord, None,
                            fields.quarternotes, fields.move_scale_max, fields.scale_preview, fields.play_background_chord, fields.repeat_n_times,
                            fields.timeout, fields.notes_range)

    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path, media_type='application/octet-stream', filename='record.wav')