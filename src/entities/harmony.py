"""

mozna decydować, czy zwracane są trzydźwięki lub czterodźwięki

"""
import json
from dataclasses import dataclass, field
from typing import List, Tuple



@dataclass
class Harmony:
    """A class holding harmony created on given harmony name and tonal key
    with methods to modify each attribute

    Attributes
    ----------
    harmony_name: str
        harmony name derived from main scales
    tonal_key: str
        tonation of harmony
    steps: List[int]
        following harmony steps based on chromatic scale
    chords_progression: List[str]
        following harmony chords names
    harmony_chords: List[Tuple[str, str]]
        pairs of chord name, chord tonation kept as list of tuples
    """

    harmony_name: str
    tonal_key : str
    steps: List[int]
    chords_progression: List[str]
    harmony_chords: List[Tuple[str, str]] = field(init=False)
        
        
    def __post_init__(self):
        
        self.harmony_chords = self.__get_harmony_chords_progression(self.tonal_key, self.chords_progression, self.steps)
        
    @staticmethod
    def load_from_json(harmony_name: str, tonal_key: str) -> "Harmony":

        with open('harmonies.json', 'r') as handler:
            harmony = json.load(handler)[harmony_name]
        
        chords_progression = harmony["progression"]
        steps = [int(elem) for elem in harmony["steps"].split(",")]

        
        return Harmony(harmony_name, tonal_key, steps, chords_progression)
        
        
        
    def __get_harmony_chords_progression(self, tonal_key: str, chords_progression: list, steps: list) -> List[Tuple[str, str]]:
        """create harmony chords progression based on given variables"""
        
        def add_interval(tonal_key: str, interval: int) -> str:
            # internal function for moving tonal key by interval
            tones = [
            'c',
            'c#',
            'd',
            'd#',
            'e',
            'f',
            'f#',
            'g',
            'g#',
            'a',
            'a#',
            'b'
        ]
            
            idx = tones.index(tonal_key)
            if idx + interval > 11:
                return tones[idx + interval - 12]
            elif idx + interval < 0:
                return tones[idx + interval + 12]
            else:
                return tones[idx + interval]

        harmony_chords = []
        for chord, interval in zip(chords_progression, steps):
            harmony_chords.append((chord, add_interval(tonal_key, interval)))
            
        return harmony_chords
            
    
    
    def modify_tonal_key(self, tonal_key: str) -> None:
        """change tonal key of the harmony"""
        self.tonal_key = tonal_key
        self.harmony_chords = self.__get_harmony_chords_progression(self.tonal_key, self.chords_progression, self.steps)
    
    def replace_chord(self, pos: int, new_chord: str) -> None:
        """replace chord on given position by the new chord"""
        self.chords_progression[pos] = new_chord
        self.harmony_chords = self.__get_harmony_chords_progression(self.tonal_key, self.chords_progression, self.steps)
    
    def modify_chord_pitch(self, pos: int, move_step: int) -> None:
        """modify chord on given position by increasing/decreasing it's pitch"""
        self.steps[pos] = self.steps[pos]  + move_step
        self.harmony_chords = self.__get_harmony_chords_progression(self.tonal_key, self.chords_progression, self.steps)
    
    def delete_chord(self, pos: int) -> None:
        """delete chord on given position"""
        del self.steps[pos]
        del self.chords_progression[pos]
        self.harmony_chords = self.__get_harmony_chords_progression(self.tonal_key, self.chords_progression, self.steps)
    
    def add_new_chord(self, step: int, new_chord: str) -> None:
        """add chord at given harmony step"""
        if step in self.steps:
            raise ValueError('There is an existing chord at this step')
        if not 0 < step < 11:
            raise ValueError('Argument step must be in range 0 and 11')
        self.steps.append(step)
        self.steps.sort()
        self.chords_progression.insert(self.steps.index(step), new_chord)
        self.harmony_chords = self.__get_harmony_chords_progression(self.tonal_key, self.chords_progression, self.steps)