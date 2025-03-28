from fastapi import APIRouter
from typing import List

from entities.structures import all_melodies


router = APIRouter()

@router.get("/all_melodies_struct/")
def all_melodies_struct() -> List[dict]:
    """Get ids and names of all melodies"""
    return all_melodies