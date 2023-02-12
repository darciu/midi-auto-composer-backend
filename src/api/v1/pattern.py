from scamp import Session
from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel
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




class RequestFields(BaseModel):
    playback_tempo: int = 3500
    midi_tempo: int = 120
    scale: str = 'mixolydian'
    scale_tonation: str = 'a'
    pattern: list = [1,2,3]
    play_upwards: bool = True
    notes_range: tuple = (40, 81)

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
    

@router.post("/pattern")
def send_file(fields: RequestFields, background_tasks: BackgroundTasks):

    tempos = (fields.playback_tempo, fields.midi_tempo)

    scale = scales.all[fields.scale]
    
    output_file_path = play_pattern(tempos, scale, fields.scale_tonation, fields.pattern, fields.play_upwards, fields.notes_range)
    
    output_file_path = convert_midi_file(output_file_path)

    background_tasks.add_task(remove_file, output_file_path)

    return FileResponse(output_file_path[:-3] + 'wav', media_type='application/octet-stream', filename='record.wav')



