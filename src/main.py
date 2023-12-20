from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import multiple_scales_multiple_chords
from api.v1 import pattern
from api.v1 import scales_one_chord
from api.v1 import intervals

from api.v1 import get_scales
from api.v1 import get_chords
from api.v1 import get_scales_chords

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
    "http://127.0.0.1:3333",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex='https://.*\.a\.run\.app/',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(multiple_scales_multiple_chords.router, prefix="/v1")
app.include_router(pattern.router, prefix="/v1")
app.include_router(scales_one_chord.router, prefix="/v1")
app.include_router(intervals.router, prefix="/v1")

app.include_router(get_scales.router, prefix="/v1/scales")
app.include_router(get_chords.router, prefix="/v1/chords")
app.include_router(get_scales_chords.router, prefix="/v1/scales_chords")

