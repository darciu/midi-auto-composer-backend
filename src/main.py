from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from midiutil import MIDIFile

import scamp

from api.v1 import chords_sequence
from api.v1 import multiple_scales_multiple_chords
from api.v1 import one_scale_one_chord
from api.v1 import pattern
from api.v1 import random_background_chords
from api.v1 import random_scales_one_chord

from api.v1.scales import get_scales
from api.v1.chords import get_chords
from api.v1.scales_chords import get_scales_chords

tags_metadata = [
    {
        "name": "play_modes",
        "description": "Different playing modes for app frontend",
    },
    {
        "name": "scales",
    },
    {
        "name":"chords"
    },
    {
        "name":'scales_chords',
        "description":"Find matching scales to a single chord or chords to a single scale"
    }
]

app = FastAPI(title='MIDI Auto Composer'
              ,openapi_tags=tags_metadata)

origins = [
    "http://localhost:3333",
    "http://127.0.0.1:3333"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(multiple_scales_multiple_chords.router, prefix="/v1")
app.include_router(one_scale_one_chord.router, prefix="/v1")
app.include_router(pattern.router, prefix="/v1")
app.include_router(random_background_chords.router, prefix="/v1")
app.include_router(random_scales_one_chord.router, prefix="/v1")

app.include_router(get_scales.router, prefix="/v1/scales")
app.include_router(get_chords.router, prefix="/v1/chords")
app.include_router(get_scales_chords.router, prefix="/v1/get_scales_chords")


@app.on_event("startup")
def update_function():
    "This is update of scamp.Performance method in order to edit a midi file"
    def save_midi_file(self, output_file_name: str, playback_tempo: int, midi_tempo: int, max_channels: int = 16,
                        ring_time: float = 0.5,  pitch_bend_range: float = 2, envelope_precision: float = 0.01) -> MIDIFile:
        midi_obj = MIDIFile(len(self.parts))        
        self.remap_to_tempo(playback_tempo)
        midi_obj.addTempo(0, 0, midi_tempo)

        for i, part in enumerate(self.parts):
            part.write_to_midi_file_track(midi_obj, i, max_channels=max_channels, ring_time=ring_time,
                                            pitch_bend_range=pitch_bend_range, envelope_precision=envelope_precision)

        if hasattr(output_file_name, 'write'):
            midi_obj.writeFile(output_file_name)
        else:
            with open(output_file_name, "wb") as output_file_name:
                midi_obj.writeFile(output_file_name)

    setattr(scamp.Performance, 'save_midi_file', save_midi_file)
