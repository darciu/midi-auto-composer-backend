from typing import List, Tuple, Optional
from enum import Enum
from pydantic import BaseModel, Field, validator, root_validator



def less_than_three_minutes(v: Optional[int]):
    if not v == None:
        if v <= 0:
            raise ValueError('timeout must be greater than zero seconds')
        elif v > 180:
            raise ValueError('timeout must be less than 180 seconds')
        
def timeout_or_repeat_n_times(cls, values: dict) -> dict:
    timeout = values.get('timeout')
    repeat_n_times = values.get('repeat_n_times')

    if (timeout is None) and (repeat_n_times is None):
        raise ValueError('one of values timeout or repeat_n_times should not be None value')
    return values


class Difficulty(str, Enum):
    ionian = "easy"
    harmonic_minor = "normal"
    melodic_minor = "hard"

class Tonation(str, Enum):
    c = "c"
    c_sharp = "c#"
    d = "d"
    d_sharp = "d#"
    e = "e"
    f = "f"
    f_sharp = "f#"
    g = "g"
    g_sharp = "g#"
    a = "a"
    a_sharp = "a#"
    b = "b"
    random = "random"


tempo_field = Field(default=120, title='Recording file tempo', ge=20, le=200)
quarternotes_field = Field(default= 4, title='How many quarternotes per measure', ge=1, le=8)
bassline_field = Field(default=True, title='Add bassline to the recording')
percussion_field = Field(default=True, title='Add percusion beat to the recording')
move_scale_max_field = Field(default= 2, title='Maximum movement through the scale steps', ge=1, le=5)
difficulty_field = Field(default='normal', title='Higher level of difficulty means that random melody notes will have greate intervals')
preview_field = Field(default=True, title='Play preview')
repeat_n_times_field = Field(default= 20, title='How many repetitions of chords sequence', ge=1, le=40)
timeout_field = Field(default=None, title='Optional timeout', nullable=True)
notes_range_field = Field(default=(40, 81), title='Scales pitch range')

class RequestFieldsChordsSequence(BaseModel):
    tempo: int = tempo_field
    chords: List[Tuple[str, str]] = Field(default=[('major', 'c'), ('dominant7', 'f')], title='Chords to play')
    quarternotes: int = quarternotes_field
    bassline: bool = bassline_field
    percussion: bool = percussion_field
    repeat_n_times: Optional[int] = repeat_n_times_field
    timeout: Optional[int] = timeout_field
    notes_range: tuple = notes_range_field

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "chords": [('major', 'c'), ('dominant7', 'f')],
                "quarternotes": 4,
                "bassline": True,
                "percussion": True,
                "repeat_n_times": 20,
                "notes_range": (40, 81)
            }
        }

    # validators

    _timeout_or_repeats = root_validator(allow_reuse=True)(timeout_or_repeat_n_times)
    _timeout_limits = validator('timeout', allow_reuse=True)(less_than_three_minutes)
    



class RequestFieldsRandomScalesOneChord(BaseModel):
    tempo: int = tempo_field
    scales: List[str] = Field(default=['pentatonic_minor','pentatonic_major'], title='Scales to play')
    chord_name: str = Field(default='major', title='Background chord name')
    tonation: Tonation = Field(default='random', title='Tonation')
    quarternotes: int = quarternotes_field
    move_scale_max: int = move_scale_max_field
    difficulty: Difficulty = difficulty_field
    bassline: bool = bassline_field
    percussion: bool = percussion_field
    repeat_n_times: Optional[int] = repeat_n_times_field
    timeout: Optional[int] = timeout_field
    notes_range: tuple = notes_range_field

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "scales": ['pentatonic_minor','pentatonic_major'],
                "chord_name":"major",
                "tonation": "random",
                "quarternotes": 4,
                "move_scale_max": 2,
                "difficulty": "normal",
                "bassline": True,
                "percussion": True,
                "repeat_n_times": 40,
                "notes_range": (40, 81)
            }
        }

    # validators

    _timeout_or_repeats = root_validator(allow_reuse=True)(timeout_or_repeat_n_times)
    _timeout_limits = validator('timeout', allow_reuse=True)(less_than_three_minutes)
    


class RequestFieldsBackgroundChords(BaseModel):
    tempo: int = tempo_field
    chords: List[Tuple[str, str]] = Field(default=[('major', 'c'), ('dominant7', 'f')], title='Chords to play')
    quarternotes: int = quarternotes_field
    bassline: bool = bassline_field
    percussion: bool = percussion_field
    repeat_n_times: Optional[int] = repeat_n_times_field
    timeout: Optional[int] = timeout_field
    notes_range: tuple = notes_range_field

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "chords": [('major', 'c'), ('dominant7', 'f')],
                "quarternotes": 4,
                "bassline": True,
                "percussion": True,
                "repeat_n_times": 20,
                "notes_range": (40, 81)
            }
        }

    # validators

    _timeout_or_repeats = root_validator(allow_reuse=True)(timeout_or_repeat_n_times)
    _timeout_limits = validator('timeout', allow_reuse=True)(less_than_three_minutes)


class RequestFieldsPattern(BaseModel):
    tempo: int = tempo_field
    pattern: list = Field(default=[1,2,3], title='Pattern to play through the chosen scale')
    scale_name: str = Field(default='mixolydian', title='Pattern will be based on this scale') 
    tonation: Tonation = Field(default='random', title='Scale tonation')
    play_upwards: bool = Field(default=True, title='Should pattern be played upwards or downwards')
    preview_pattern: bool = preview_field
    pause_between: bool = Field(default=True, title='There is always one quarternote pause added between pattern played')
    notes_range: tuple = notes_range_field

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


class RequestFieldsOneScaleOneChord(BaseModel):
    tempo: int = tempo_field
    scale_name: str = Field(default='mixolydian', title='Scale to be played')
    chord_name: str = Field(default='major', title='Background chord')
    tonation: Tonation = Field(default='random', title='Tonation')
    quarternotes: int = quarternotes_field
    move_scale_max: int = move_scale_max_field
    difficulty: Difficulty = difficulty_field
    bassline: bool = bassline_field
    percussion: bool = percussion_field
    scale_preview: bool = preview_field
    repeat_n_times: Optional[int] = repeat_n_times_field
    timeout: Optional[int] = timeout_field
    notes_range: tuple = notes_range_field

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "scale_name": 'mixolydian',
                "chord_name":"major",
                "tonation": "random",
                "quarternotes": 4,
                "move_scale_max": 2,
                "difficulty": "normal",
                "bassline": True,
                "percussion": True,
                "scale_preview": True,
                "repeat_n_times": 40,
                "notes_range": (40, 81)
            }
        }

    # validators

    _timeout_or_repeats = root_validator(allow_reuse=True)(timeout_or_repeat_n_times)
    _timeout_limits = validator('timeout', allow_reuse=True)(less_than_three_minutes)

class RequestFieldsMultipleScalesMultipleChords(BaseModel):
    tempo: int = tempo_field
    scales = Field(default=[('ionian','d'),('dorian','e')], title='List of tuples: scale - tonation to be played')
    chords = Field(default=[('major','d'),('minor','e')], title='List of tuples: chord - tonation to be played')
    quarternotes: int = quarternotes_field
    move_scale_max: int = move_scale_max_field
    difficulty: Difficulty = difficulty_field
    bassline: bool = bassline_field
    percussion: bool = percussion_field
    repeat_n_times: Optional[int] = repeat_n_times_field
    timeout: Optional[int] = timeout_field
    notes_range: tuple = notes_range_field

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "scales": [('ionian','d'),('dorian','e')],
                "chords": [('major','d'),('minor','e')],
                "move_scale_max": 2,
                "difficulty": "normal",
                "bassline": True,
                "percussion": True,
                "repeat_n_times": 20,
                "notes_range": (40, 81)
            }
        }

    # validators

    _timeout_or_repeats = root_validator(allow_reuse=True)(timeout_or_repeat_n_times)
    _timeout_limits = validator('timeout', allow_reuse=True)(less_than_three_minutes)