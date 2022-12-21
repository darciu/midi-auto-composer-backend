from dataclasses import dataclass
from typing import Dict, List
import json

@dataclass
class Chords:
    """A class holding chords in dictionary if form
    chord type (str) : list of integer steps

    where steps are following building chord pitches
    eg. "major": [0,4,7]

    Attributes
    ----------
    chords: dict
        chords stored as dictionary
    """
    chords: Dict[str, List[int]]

    @staticmethod
    def load_chords() -> "Chords":

        with open('static/chords.json', 'r') as handler:
            chords = json.load(handler)

        chords = {name: [int(step) for step in struct.split(',')] for name, struct in chords.items()}

        return Chords(chords)
