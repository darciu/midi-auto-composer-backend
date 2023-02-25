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

@router.get("/scale_by_name/{scale_name}", summary='Scale by name')
def scale_by_name(scale_name) -> list:
    """Get scale steps by scale name"""
    if scales.all.get(scale_name) == None:
        raise HTTPException(status_code=404, detail="Invalid scale's name!")
    return scales.all.get(scale_name)

@router.get("/all_scales_names/",summary='All scales names')
def all_scales_names() -> List[str]:
    """Get list of all available scales filtering by parameters"""
    return list(scales.all.keys())

@router.get("/all_scales_names_seven_tone/")
def all_scales_names_seven_tone() -> List[str]:
    """Get list of all seven tones scales"""
    return list(scales.seven_tone.keys())

@router.get("/all_scales_names_six_tone/")
def all_scales_names_six_tone() -> List[str]:
    """Get list of all six tones scales"""
    return list(scales.six_tone.keys())

@router.get("/all_scales_names_pentatonic/")
def all_scales_names_pentatonic() -> List[str]:
    """Get list of all pentatonic scales"""
    return list(scales.pentatonic.keys())

@router.get("/all_modals_names/")
def all_modals() -> List[str]:
    """Get list of all modals names"""
    return list(scales.modal_by_name.keys())

@router.get("/modal_sub_names/{modal_name}")
def modal_sub_names(modal_name: AllModals) -> List[str]:
    """Get list of all scales names by given modal name"""
    if scales.modal_by_name.get(modal_name) == None:
        raise HTTPException(status_code=404, detail="Invalid modal's name!")
    return list(scales.modal_by_name.get(modal_name).keys())