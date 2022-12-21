from dataclasses import dataclass, field
from src.entities.scales import Scales
from src.entities.chords import Chords

@dataclass
class ScalesChords:

    scales: Scales
    chords: Chords
    chords_scales: dict = field(init=False)
    scales_chords: dict = field(init=False)
    def __post_init__(self):

        self.chords_scales = self.__chords_scales()
        self.scales_chords = self.__scales_chords()
        
    @staticmethod
    def create_object(path_scales:str = None, path_chords: str = None) -> "ScalesChords":
        
        if path_scales == None:
            path_scales = 'static/scales.json'
        if path_chords == None:
            path_chords = 'static/chords.json'

        scales = Scales.load_scales(path_scales)
        chords = Chords.load_chords()

        return ScalesChords(scales, chords)
    
    def __chords_scales(self) -> dict:
        full_dict = {}

        for chord_name, chord_steps in self.chords.chords.items():
            chord_steps_set = set(chord_steps)
            matching_scales = {}
            for scale_name, scale_steps in self.scales.all.items():

                scale_steps_set = set(scale_steps)
                if chord_steps_set.intersection(scale_steps_set) == chord_steps_set:
                    matching_scales.update({scale_name:scale_steps})

            full_dict.update({chord_name: {"steps":chord_steps,"matching_scales":matching_scales}})
            
        return full_dict
        
    def __scales_chords(self) -> dict:
        
        full_dict = {}

        for scale_name, scale_steps in self.scales.all.items():
            scale_steps_set = set(scale_steps)
            matching_chords = {}
            for chord_name, chord_steps in self.chords.chords.items():

                chord_steps_set = set(chord_steps)
                if chord_steps_set.intersection(scale_steps_set) == chord_steps_set:
                    matching_chords.update({chord_name:chord_steps})

            full_dict.update({scale_name: {"steps":scale_steps,"matching_chords":matching_chords}})

        return full_dict