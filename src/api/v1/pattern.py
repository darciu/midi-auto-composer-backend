from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel, Field
import random



from play_functions.scale_with_pattern import play_scale_with_pattern_upwards, play_scale_with_pattern_downwards
from . import remove_file, convert_midi_file

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords

scales = Scales.load()
chords = Chords.load()
scales_chords = ScalesChords.load()

router = APIRouter()




class RequestFieldsPattern(BaseModel):
    playback_tempo: int = Field(default=3500)
    midi_tempo: int = Field(default=120, title='Recording file tempo')
    scale: str = Field(default='mixolydian', title='Pattern will be based on this scale') 
    scale_tonation: str = Field(default='random', title='Scale tonation')
    pattern: list = Field(default=[1,2,3], title='Pattern to play through the chosen scale')
    play_upwards: bool = Field(default=True, title='Should pattern be played upwards or downwards')
    notes_range: tuple = Field(default=(40, 81), title='Scales pitch range')

    class Config:
        schema_extra = {
            "example": {
                "playback_tempo": 3500,
                "midi_tempo": 120,
                "scale": 'mixolydian',
                "scale_tonation": "random",
                "quarternotes": 4,
                "play_upwards": True,
                "notes_range": (40, 81)
            }
        }

def play_pattern(tempos: tuple, scale: list, scale_tonation: str, pattern: list, play_upwards: bool, notes_range: tuple) -> str:

    playback_tempo = tempos[0]
    midi_tempo = tempos[1]

    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    sess.start_transcribing()

    if play_upwards:

        play_scale_with_pattern_upwards(instrument_solo, scale, scale_tonation, pattern, notes_range)

    else:

        play_scale_with_pattern_downwards(instrument_solo, scale, scale_tonation, pattern, notes_range)

    sess.stop_transcribing().save_midi_file(output_file_path, playback_tempo, midi_tempo)

    return output_file_path
    

@router.post("/pattern", tags=['play_modes'])
def pattern(fields: RequestFieldsPattern, background_tasks: BackgroundTasks):
    """Playing pattern on scale basis"""
    tempos = (fields.playback_tempo, fields.midi_tempo)

    scale = scales.all[fields.scale]
    
    output_file_path = play_pattern(tempos, scale, fields.scale_tonation, fields.pattern, fields.play_upwards, fields.notes_range)
    
    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path[:-3] + 'wav', media_type='application/octet-stream', filename='record.wav')



