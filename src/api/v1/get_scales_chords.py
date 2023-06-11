from fastapi import APIRouter, HTTPException

from entities.scales_chords import ScalesChords



scales_chords = ScalesChords.load()

router = APIRouter()

@router.get("/scales_matching_chord/{chord_name}", tags=['scales_chords'])
def scales_matching_chord(chord_name: str) -> dict:
    """Get all scales matching given chord"""
    if scales_chords.chord_scales.get(chord_name) == None:
        raise HTTPException(status_code=404, detail="Invalid chord's name!")
    
    return scales_chords.scales.get_details([*scales_chords.chord_scales.get(chord_name)['matching_scales']])


@router.get("/chords_matching_scale/{scale_name}", tags=['scales_chords'])
def chords_matching_scale(scale_name: str) -> dict:
    """Get all chords matching given scale"""
    if scales_chords.scale_chords.get(scale_name) == None:
        raise HTTPException(status_code=404, detail="Invalid scale's name!")
    return scales_chords.chords.get_details([*scales_chords.scale_chords.get(scale_name)['matching_chords']])

