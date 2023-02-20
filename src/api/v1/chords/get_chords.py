from fastapi import APIRouter
from typing import List
from pydantic import Field, BaseModel

from entities.chords import Chords

chords = Chords.load()

router = APIRouter()

@router.get("/chord_by_name/{chord_name}")
def chord_by_name(chord_name: str) -> list:
    """Get chord steps by chord name"""
    return chords.all.get(chord_name, ValueError('There is no such a chord!'))

@router.get("/all_chords_names/")
def all_chords_names() -> List[str]:
    """Get list of all available chords"""
    return list(chords.all.keys())