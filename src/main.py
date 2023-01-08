from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from midiutil import MIDIFile

import scamp

app = FastAPI()

from api.v1 import multiple_scales_multiple_chords

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(multiple_scales_multiple_chords.router, prefix="/v1")


@app.on_event("startup")
def update_function():
    def get_midi_object(self, playback_tempo: int, midi_tempo: int, max_channels: int = 16,
                            ring_time: float = 0.5,  pitch_bend_range: float = 2, envelope_precision: float = 0.01) -> MIDIFile:
        midi_obj = MIDIFile(len(self.parts))        
        self.remap_to_tempo(playback_tempo)
        midi_obj.addTempo(0, 0, midi_tempo)

        for i, part in enumerate(self.parts):
            part.write_to_midi_file_track(midi_obj, i, max_channels=max_channels, ring_time=ring_time,
                                            pitch_bend_range=pitch_bend_range, envelope_precision=envelope_precision)

        return midi_obj


    
    setattr(scamp.Performance, 'get_midi_object', get_midi_object)
