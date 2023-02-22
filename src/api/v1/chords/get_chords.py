from fastapi import APIRouter, HTTPException
from typing import List

from entities.chords import Chords

chords = Chords.load()

router = APIRouter()

@router.get("/chord_by_name/{chord_name}")
def chord_by_name(chord_name: str) -> list:
    """Get chord steps by chord name"""
    if chords.all.get(chord_name) == None:
        raise HTTPException(status_code=404, detail="Invalid chord's name!")
    return chords.all.get(chord_name)

@router.get("/all_chords_names/")
def all_chords_names() -> List[str]:
    """Get list of all available chords"""
    return list(chords.all.keys())