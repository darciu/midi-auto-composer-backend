from os import environ

if environ.get('FRONTEND_URL') is None:
    from config import FRONTEND_URL
else:
    FRONTEND_URL = environ.get('FRONTEND_URL')


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1 import custom_creator
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


# @app.middleware("http")
# async def add_cors_headers(request, call_next):
#     response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = "https://midi-auto-composer-front-bsnougc45q-lz.a.run.app, https://midi-auto-composer-frontend-bsnougc45q-ew.a.run.app, https://audiotrainer.pl, http://localhost:3333, http://127.0.0.1:3333"
#     response.headers["Access-Control-Allow-Credentials"] = "true"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     return response

origins = [
    "https://midi-auto-composer-front-bsnougc45q-lz.a.run.app",
    "https://midi-auto-composer-frontend-bsnougc45q-ew.a.run.app",
    "https://audiotrainer.pl",
    "http://localhost:3333",
    "http://127.0.0.1:3333",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(pattern.router, prefix="/v1")
app.include_router(intervals.router, prefix="/v1")
app.include_router(scales_one_chord.router, prefix="/v1")
app.include_router(custom_creator.router, prefix="/v1")


app.include_router(get_scales.router, prefix="/v1/scales")
app.include_router(get_chords.router, prefix="/v1/chords")
app.include_router(get_scales_chords.router, prefix="/v1/scales_chords")

@app.get('dummy/')
def dummy():
    return environ.get('DUMMY')