from typing import List, Tuple, Optional
from pydantic import BaseModel, Field, validator


tempo_field = Field(default=120, title='Recording file tempo', ge=20, le=200)
quarternotes_field = Field(default= 4, title='How many quarternotes per measure', ge=1, le=8)
bassline_field = Field(default=True, title='Add bassline to the recording')
percussion_field = Field(default=True, title='Add percusion beat to the recording')
repeat_n_times_field = Field(default= 20, title='How many repetitions of chords sequence', ge=1, le=40)
timeout_field = Field(default=None, title='Optional timeout', nullable=True)
notes_range_field = Field(default=(40, 81), title='Scales pitch range')

class RequestFieldsChordsSequence(BaseModel):
    tempo: int = tempo_field
    chords: List[Tuple[str, str]] = Field(default=[('major', 'c'), ('dominant7', 'f')], title='Chords to play')
    quarternotes: int = quarternotes_field
    bassline: bool = bassline_field
    percussion: bool = percussion_field
    repeat_n_times: int = repeat_n_times_field
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

    @validator('timeout')
    def less_than_three_minutes(cls, v):
        if not v == None:
            if v <= 0:
                raise ValueError('timeout must be greater than zero seconds')
            elif v > 180:
                raise ValueError('timeout must be less than 180 seconds')

    # dodać walidację na repeat_n_times obliczane w zależności od quarternotes i ilości taktów