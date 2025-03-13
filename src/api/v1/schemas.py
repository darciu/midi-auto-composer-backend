from typing import List, Tuple, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field, conlist, validator



class Difficulty(str, Enum):
    easy = "easy"
    normal = "normal"
    hard = "hard"

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



tempo_field = Field(default=120, title='Recording file tempo', ge=60, le=150)
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


class RequestFieldsPattern(BaseModel):
    tempo: int = Field(default=120, title='Recording file tempo', ge=80, le=150)
    pattern: conlist(int, min_items=1, max_items=5) = Field(default=[1,2,3], title='Pattern to play through the chosen scale')
    tempo: int = Field(default=120, title='Recording file tempo', ge=80, le=150)
    pattern: conlist(int, min_items=1, max_items=5) = Field(default=[1,2,3], title='Pattern to play through the chosen scale')
    scale_name: str = Field(default='mixolydian', title='Pattern will be based on this scale') 
    tonation: Tonation = Field(default='random', title='Scale tonation')
    play_upwards: bool = Field(default=True, title='Pattern is played upwards or downwards')
    play_upwards: bool = Field(default=True, title='Pattern is played upwards or downwards')
    preview_pattern: bool = preview_field
    pause_between: bool = Field(default=True, title='There is always one quarternote pause added between pattern played')
    notes_range: tuple = notes_range_field

    class Config:
        schema_extra = {
            "example": {
                "tempo": 120,
                "pattern":[1,2,3],
                "pattern":[1,2,3],
                "scale_name": 'mixolydian',
                "tonation": "random",
                "play_upwards": True,
                "preview_pattern": True,
                "pause_between": True,
                "notes_range": (40, 70),
            }
        }



class RequestFieldsScalesOneChord(BaseModel):
    tempo: int = Field(default=50, title='Recording file tempo', ge=20, le=80)
    scales_names: List[str] = Field(default=['pentatonic_minor','pentatonic_major'], title='Scales to play')
    chord_name: str = Field(default='major', title='Background chord name')
    tonation: Tonation = Field(default='random', title='Tonation')
    quarternotes: int = quarternotes_field
    move_scale_max: int = move_scale_max_field
    difficulty: Difficulty = difficulty_field
    bassline: bool = bassline_field
    percussion: bool = percussion_field
    random_sequence: bool = Field(default=True, title='Play scales randomly or sequentially')
    notes_range: tuple = notes_range_field

    class Config:
        schema_extra = {
            "example": {
                "tempo": 50,
                "scales_names": ['pentatonic_minor','pentatonic_major'],
                "chord_name":"major",
                "tonation": "random",
                "quarternotes": 4,
                "move_scale_max": 2,
                "difficulty": "normal",
                "bassline": True,
                "percussion": True,
                "random_sequence": True,
                "notes_range": (40, 81)
            }
        }


class RequestFieldsCustomCreator(BaseModel):
    tempo: int = Field(default=50, title='Recording file tempo', ge=20, le=80)
    # tonation, quarternotes, scale_name, chord_name
    components: List[dict] = Field(title = 'Component block representing one measure' )
    move_scale_max: int = move_scale_max_field
    difficulty: Difficulty = difficulty_field
    repeat_n_times: int = Field(default=2, title='Repeat sequence n times', ge=1, le=5) 
    bassline: bool = bassline_field
    percussion: bool = percussion_field
    notes_range: tuple = notes_range_field

    class Config:

        components = [
                        {
                            "order":1,
                            "tonation":"a",
                            "quarternotes":4,
                            "scale_name":"ionian",
                            "chord_name":"major"
                        },
                        {
                            "order":2,
                            "tonation":"c",
                            "quarternotes":4,
                            "scale_name":"mixolydian",
                            "chord_name":"major"
                        },
                        {
                            "order":3,
                            "tonation":"d",
                            "quarternotes":2,
                            "scale_name":"aeolian",
                            "chord_name":"minor"
                        }
                    ]
        schema_extra = {
            "example": {
                "tempo": 70,
                "components": components,
                "move_scale_max": 2,
                "difficulty": "normal",
                "repeat_n_times": 5,
                "bassline": True,
                "percussion": True,
                "notes_range": (40, 81)
            }
        }


class RequestFieldsIntervals(BaseModel):
    tempo: int = Field(default=30, title='Recording file tempo', ge=20, le=80)
    intervals: List[str] = Field(default=['m2','M2','TT'], title='Repeat sequence n times',) 
    difficulty: Difficulty = difficulty_field
    notes_range: tuple = notes_range_field

    @validator('intervals')
    def must_be_in_intervals(cls,intervals):
      valid_intervals=['m2','M2','m3','M3','P4','TT','P5','m6','M6','m7','M7','P8']
      for interval in intervals:
        if interval not in valid_intervals:    
            raise ValueError(f'Value {interval} must be in {valid_intervals}')
      return intervals
    
    class Config:
        schema_extra = {
            "example": {
                "tempo": 30,
                "intervals": ['m2','M2','TT'],
                "difficulty": "normal",
                "notes_range": (40, 81)
            }
        }

class RequestFieldsMelody(BaseModel):
    tempo: int = Field(default=70, title='Recording file tempo', ge=40, le=120)
    tonation: Tonation = Field(default='random', title='Tonation')
    melody_id: str = "1"
    notes_range: tuple = notes_range_field
    
    class Config:
        schema_extra = {
            "example": {
                "tempo": 70,
                "tonation": "e",
                "melody_id": "1",
                "notes_range": (40, 81)
            }
        }