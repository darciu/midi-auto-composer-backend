from fastapi import APIRouter


from entities.structures import all_melodies


router = APIRouter()

@router.get("/melodies_id_name/")
def melodies_id_name() -> dict:
    """Get ids and names of all melodies"""
    return {key:all_melodies[key]['name'] for key in all_melodies.keys()}