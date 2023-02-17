from fastapi import APIRouter
from typing import List

from entities.chords import Chords

chords = Chords.load()

router = APIRouter()

@router.get("/chord_by_name/")
def chord_by_name(chord_name: str) -> list:
    """Get chord steps by chord name
    
    :param chord_name: chord's name
    :type chord_name: str
    :return: chord's steps progression
    """
    return chords.all.get(chord_name, ValueError('There is no such a chord!'))

@router.get("/all_chords_names/")
def all_chords_names() -> List[str]:
    """Get list of all available chords
    
    :return: list of all chords names
    """
    return list(chords.all.keys())