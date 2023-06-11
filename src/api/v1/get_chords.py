from fastapi import APIRouter, HTTPException, Query
from typing import List

from entities.chords import Chords

chords = Chords.load()

router = APIRouter()

@router.get("/chord_by_name/{chord_name}", tags=['chords'])
def chord_by_name(chord_name: str) -> dict:
    """Get chord steps by chord name"""
    if chords.detailed.get(chord_name, None) == None:
        raise HTTPException(status_code=404, detail="Invalid chord's name!")
    return chords.detailed.get(chord_name)


@router.get("/all_chords/", tags=['chords'])
def all_chords() -> dict:
    """Get list of all available chords"""
    return chords.get_details(chords.all)


@router.get("/filter_chords/", tags=['chords'])
def filter_chords(chords_types: list = Query(default=[])) -> List[str]:
    """Selects chords by providing filters list as chords types (strings)
    
    Parameters
    ----------
    chords_types : list[str]
        List of strings of chords types. Available chord types: major, minor, dimished_fifth, perfect_fifth,
            augmented_fifth, minor_seventh, major_seventh.
    """

    for chord_type in chords_types:
        if chord_type not in ['major', 'minor', 'dimished_fifth', 'perfect_fifth', 'augmented_fifth', 'minor_seventh', 'major_seventh']:
            raise HTTPException(status_code=404, detail="Invalid chord's type!")

    return chords.filter_chords(chords_types)


