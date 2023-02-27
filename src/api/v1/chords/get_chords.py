from fastapi import APIRouter, HTTPException, Query
from typing import List, Union

from entities.chords import Chords

chords = Chords.load()

router = APIRouter()

@router.get("/chord_by_name/{chord_name}", tags=['chords'])
def chord_by_name(chord_name: str) -> List[int]:
    """Get chord steps by chord name"""
    if chords.all.get(chord_name) == None:
        raise HTTPException(status_code=404, detail="Invalid chord's name!")
    return chords.all.get(chord_name)


@router.get("/all_chords_names/", tags=['chords'])
def all_chords_names() -> List[str]:
    """Get list of all available chords"""
    return list(chords.all.keys())


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

    return list(chords.filter_chords(chords_types).keys())


