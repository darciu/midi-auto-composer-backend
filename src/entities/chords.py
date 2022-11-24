from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass
class Chords:
    chords: Dict[str,List[int]]

    @staticmethod
    def load_chords(path: Optional[str] = None) -> "Chords":
        if path == None:
            path = 'static/chords.json'
        with open(path, 'r') as handler:
            chords = json.load(handler)

        chords = {name:[int(step) for step in struct.split(',')] for name, struct in chords.items()}

        return Chords(chords)
