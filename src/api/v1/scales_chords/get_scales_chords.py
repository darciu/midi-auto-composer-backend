from fastapi import APIRouter
from pydantic import Field, BaseModel

from entities.scales_chords import ScalesChords



scales_chords = ScalesChords.load()

router = APIRouter()

@router.get("/scales_matching_chord/{chord_name}")
def scale_by_name(chord_name: str) -> list:
    """Get all scales matching given chord"""

    return [*scales_chords.chord_scales.get(chord_name, ValueError('There is no such a chord!'))['matching_scales']]


@router.get("/chords_matching_scale/{scale_name}")
def scale_by_name(scale_name: str) -> list:
    """Get all chords matching given scale"""

    return [*scales_chords.scale_chords.get(scale_name, ValueError('There is no such a scale!'))['matching_chords']]

