from fastapi import APIRouter, HTTPException
from typing import List
from enum import Enum

from entities.scales import Scales


class AllModals(str, Enum):
    ionian = "ionian"
    harmonic_minor = "harmonic_minor"
    melodic_minor = "melodic_minor"
    harmonic_major = "harmonic_major"
    double_harmonic_major = "double_harmonic_major"
    pentatonic_major = "pentatonic_major"


scales = Scales.load()
router = APIRouter()

@router.get("/scale_by_name/{scale_name}", tags=['scales'])
def scale_by_name(scale_name) -> dict:
    """Get scale steps by scale name"""
    if scales.detailed.get(scale_name, None) == None:
        raise HTTPException(status_code=404, detail="Invalid scale's name!")
    return scales.detailed.get(scale_name)

@router.get("/all_scales/", tags=['scales'])
def all_scales() -> dict:
    """Get all available scales"""
    return scales.get_details(scales.all)

@router.get("/seven_tone/", tags=['scales'])
def seven_tone() -> dict:
    """Get list of all seven tones scales"""
    return scales.get_details(scales.seven_tone)
    
@router.get("/six_tone/", tags=['scales'])
def six_tone() -> dict:
    """Get list of all six tones scales"""
    return scales.get_details(scales.six_tone)

@router.get("/pentatonic/", tags=['scales'])
def pentatonic() -> dict:
    """Get list of all pentatonic scales"""
    return scales.get_details(scales.pentatonic)

@router.get("/all_modals_names/", tags=['scales'])
def all_modals_names() -> List[str]:
    """Get list of all modals names"""
    return list(scales.modals.keys())

@router.get("/modal_sub_names/{modal_name}", tags=['scales'])
def modal_sub_names(modal_name: AllModals) -> List[str]:
    """Get list of all scales names by given modal name"""
    if scales.modals.get(modal_name) == None:
        raise HTTPException(status_code=404, detail="Invalid modal's name!")
    return list(scales.modals.get(modal_name))