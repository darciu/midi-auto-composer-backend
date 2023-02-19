from fastapi import APIRouter
from pydantic import Field

from entities.scales_chords import ScalesChords

scales_chords = ScalesChords.load()

router = APIRouter()

@router.get("/scales_matching_chord/")
def scale_by_name(chord_name: str = Field(description="Chord's name")) -> list:
    """Get all scales matching given chord"""

    return [*scales_chords.chord_scales.get(chord_name, ValueError('There is no such a chord!'))['matching_scales']]


@router.get("/chords_matching_scale/")
def scale_by_name(scale_name: str = Field(description="Scale's name")) -> list:
    """Get all chords matching given scale"""

    return [*scales_chords.scale_chords.get(scale_name, ValueError('There is no such a scale!'))['matching_chords']]

