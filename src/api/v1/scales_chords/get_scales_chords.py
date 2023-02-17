from fastapi import APIRouter
from typing import List

from entities.scales_chords import ScalesChords

scales_chords = ScalesChords.load()

router = APIRouter()

@router.get("/scales_matching_chord/")
def scale_by_name(chord_name: str) -> list:
    """Get all scales matching given chord
    
    :param chord_name: chord's name
    :type chord_name: str
    :return: list of scales
    """

    return [*scales_chords.chord_scales.get(chord_name, ValueError('There is no such a chord!'))['matching_scales']]


@router.get("/chords_matching_scale/")
def scale_by_name(scale_name: str) -> list:
    """Get all chords matching given scale
    
    :param scale_name: scale's name
    :type scale_name: str
    :return: list of chords
    """

    return [*scales_chords.scale_chords.get(scale_name, ValueError('There is no such a scale!'))['matching_chords']]

