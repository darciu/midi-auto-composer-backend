from fastapi import APIRouter
from typing import List

from entities.scales import Scales

scales = Scales.load()

router = APIRouter()

@router.get("/scale_by_name/")
def scale_by_name(scale_name: str) -> list:
    """Get scale steps by scale name"""
    return scales.all.get(scale_name, ValueError('There is no such a scale!'))

@router.get("/all_scales_names/")
def all_scales_names() -> List[str]:
    """Get list of all available scales"""
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

@router.get("/all_modals/")
def all_modals() -> List[str]:
    """Get list of all modals"""
    return list(scales.modal_by_name.keys())

@router.get("/modal_sub_names/")
def modal_sub_names(modal_name) -> List[str]:
    """Get list of all scales by modal name"""
    return list(scales.modal_by_name.get(modal_name, ValueError('No such a modal!')).keys())