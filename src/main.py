from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from midiutil import MIDIFile

import scamp

from api.v1 import chords_sequence
from api.v1 import multiple_scales_multiple_chords
from api.v1 import one_scale_one_chord
from api.v1 import pattern
from api.v1 import random_background_chords
from api.v1 import random_scales_one_chord

from api.v1.scales import get_scales

app = FastAPI()

origins = [
    "http://localhost:3333"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(multiple_scales_multiple_chords.router, prefix="/v1")
app.include_router(one_scale_one_chord.router, prefix="/v1")
app.include_router(pattern.router, prefix="/v1")
app.include_router(random_background_chords.router, prefix="/v1")
app.include_router(random_scales_one_chord.router, prefix="/v1")

app.include_router(get_scales.router, prefix="/v1/scales")



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
