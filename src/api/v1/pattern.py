from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel, Field
import random



from play_functions.scale_with_pattern import play_scale_with_pattern_upwards, play_scale_with_pattern_downwards
from play_functions.helper_functions import get_tonation
from . import remove_file, convert_midi_file

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords
from entities.midi_composer import MIDIComposer

scales = Scales.load()
chords = Chords.load()
scales_chords = ScalesChords.load()

router = APIRouter()




class RequestFieldsPattern(BaseModel):
    tempo: int = Field(default=120, title='Recording file tempo')
    pattern: list = Field(default=[1,2,3], title='Pattern to play through the chosen scale')
    scale_name: str = Field(default='mixolydian', title='Pattern will be based on this scale') 
    tonation: str = Field(default='random', title='Scale tonation')
    play_upwards: bool = Field(default=True, title='Should pattern be played upwards or downwards')
    preview_pattern: bool = Field(default=True, title='Play pattern preview')
    pause_between: bool = Field(default=True, title='There is always one quarternote pause added between pattern played')
    notes_range: tuple = Field(default=(40, 81), title='Scales pitch range')

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "scale_name": 'mixolydian',
                "tonation": "random",
                "play_upwards": True,
                "preview_pattern": True,
                "pause_between": True,
                "notes_range": (40, 81)
            }
        }

def play_pattern(tempo: int, pattern: list, scale_name: str, tonation: str, play_upwards: bool, preview_pattern: bool, pause_between: bool, notes_range: tuple) -> str:

    tonation = get_tonation(tonation)

    midi_composer = MIDIComposer(tempo, 1, notes_range)

    midi_composer.add_scale_pattern_part(pattern, scale_name, tonation, play_upwards, preview_pattern, pause_between)

    output_file_path = f'midi_storage/rec_{random.getrandbits(16)}.mid'

    midi_composer.midi_to_file(output_file_path)

    midi_composer.close_midi()

    return output_file_path
    

@router.post("/pattern", tags=['play_modes'])
def pattern(fields: RequestFieldsPattern, background_tasks: BackgroundTasks):
    """Playing pattern on scale basis"""
        
    output_file_path = play_pattern(fields.tempo, fields.pattern, fields.scale_name, fields.tonation, fields.play_upwards, fields.preview_pattern, fields.pause_between, fields.notes_range)
    
    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path[:-3] + 'wav', media_type='application/octet-stream', filename='record.wav')



