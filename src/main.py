from os import environ

if environ.get('FRONTEND_URL') is None:
    from config import FRONTEND_URL
else:
    FRONTEND_URL = environ.get('FRONTEND_URL')


username_secret = environ.get('USERNAME','username')
password_secret = environ.get('PASSWORD','password')

import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, UJSONResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html


from api.v1 import custom_creator
from api.v1 import pattern
from api.v1 import scales_one_chord
from api.v1 import intervals
from api.v1 import melodies
from api.v1 import get_melodies

from api.v1 import get_scales
from api.v1 import get_chords
from api.v1 import get_scales_chords

security = HTTPBasic()

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
              ,openapi_tags=tags_metadata
              ,docs_url=None
              ,redoc_url=None
              ,openapi_url="/api/openapi.json"
              ,default_response_class=UJSONResponse
              )


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = f"{FRONTEND_URL}, https://audiotrainer.pl, http://localhost:3333, http://127.0.0.1:3333"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

origins = [
    FRONTEND_URL,
    "https://audiotrainer.pl",
    "http://localhost:3333",
    "http://127.0.0.1:3333",
    FRONTEND_URL,
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
app.include_router(melodies.router, prefix="/v1")
app.include_router(get_melodies.router, prefix="/v1")

app.include_router(get_scales.router, prefix="/v1/scales")
app.include_router(get_chords.router, prefix="/v1/chords")
app.include_router(get_scales_chords.router, prefix="/v1/scales_chords")

@app.get('/dummy')
def dummy():
    return environ.get('DUMMY')


def get_username(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_username = secrets.compare_digest(credentials.username, username_secret)
    correct_password = secrets.compare_digest(credentials.password, password_secret)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/docs", response_class=HTMLResponse)
async def get_docs(username: str = Depends(get_username)):
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


@app.get("/redoc", response_class=HTMLResponse)
async def get_redoc(username: str = Depends(get_username)):
    return get_redoc_html(openapi_url="/api/openapi.json", title="redoc")

