from dataclasses import dataclass
from typing import Dict, List
from structures import all_chords



@dataclass
class Chords:
    """A class holding chords in dictionaries in form:
    chord type (str) : list of integer steps

    where steps are following building chord pitches
    eg. "major": [0,4,7]

    Attributes
    -----------
    all: dict
        all chords stored as dictionary
    minor: dict
        minor third chords stored as dictionary
    major: dict
        major third chords stored as dictionary
    dimished_fifth: dict
        dimished_fifth third chords stored as dictionary
    perfect_fifth: dict
        perfect_fifth third chords stored as dictionary
    augmented_fifth: dict
        augmented_fifth third chords stored as dictionary
    minor_seventh: dict
        minor_seventh third chords stored as dictionary
    major_seventh: dict
        major_seventh third chords stored as dictionary
    """
    all: Dict[str, List[int]]
    minor: Dict[str, List[int]]
    major: Dict[str, List[int]]
    dimished_fifth: Dict[str, List[int]]
    perfect_fifth: Dict[str, List[int]]
    augmented_fifth: Dict[str, List[int]]
    minor_seventh: Dict[str, List[int]]
    major_seventh: Dict[str, List[int]]

    @staticmethod
    def load() -> "Chords":
        """Create Chords class object from static dictionary"""

        all = {name: struct for name, struct in all_chords.items()}
        minor = {name: struct for name, struct in all_chords.items() if 3 in struct}
        major = {name: struct for name, struct in all_chords.items() if 4 in struct}
        dimished_fifth = {name: struct for name, struct in all_chords.items() if 6 in struct}
        perfect_fifth = {name: struct for name, struct in all_chords.items() if 7 in struct}
        augmented_fifth = {name: struct for name, struct in all_chords.items() if 8 in struct}
        minor_seventh = {name: struct for name, struct in all_chords.items() if 10 in struct}
        major_seventh = {name: struct for name, struct in all_chords.items() if 11 in struct}

        return Chords(all, minor, major, dimished_fifth, perfect_fifth, augmented_fifth, minor_seventh, major_seventh)
