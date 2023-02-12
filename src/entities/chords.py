from dataclasses import dataclass
from typing import Dict, List
from .structures.chords import all_chords



@dataclass
class Chords:
    """A class holding chords in dictionary in form:
    chord type (str) : list of integer steps

    where steps are following building chord pitches
    eg. "major": [0,4,7]

    Attributes:
    all: dict
        all chords stored as dictionary
    """
    all: Dict[str, List[int]]

    @staticmethod
    def load_chords() -> "Chords":

        all = {name: [int(step) for step in struct.split(',')] for name, struct in all_chords.items()}

        return Chords(all)
