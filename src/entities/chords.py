from dataclasses import dataclass
from typing import Dict
import json

@dataclass
class Chords:
    chords: Dict[str:list]

    @staticmethod
    def load_chords(path) -> "Chords":
        with open(path, 'r') as handler:
            chords = json.load(handler)

        chords = {name:struct.split(',') for name, struct in chords.items()}

        return Chords(chords)
