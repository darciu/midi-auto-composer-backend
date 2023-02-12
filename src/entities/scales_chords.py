from dataclasses import dataclass, field
from entities.scales import Scales
from entities.chords import Chords


@dataclass
class ScalesChords:
    """A class combining Scales and Chords classes also providing dictionaries which scales
    matches to particular chord and vice versa, what chords matches to particular scale


    Attributes:
    scales - a Scales class object
    chords - a Chords class object
    chord_scales - a dictionary containing every chord with all scales matches to it
    scale_chords - a dictionary containing every scale with all chords matches to it
    """

    scales: Scales
    chords: Chords
    chord_scales: dict = field(init=False)
    scale_chords: dict = field(init=False)

    def __post_init__(self):

        self.chord_scales = self.__chords_scales()
        self.scale_chords = self.__scales_chords()

    @staticmethod
    def load() -> "ScalesChords":
        """Create ScalesChords class object"""

        scales = Scales.load()
        chords = Chords.load()

        return ScalesChords(scales, chords)

    def __chords_scales(self) -> dict:
        full_dict = {}

        for chord_name, chord_steps in self.chords.all.items():
            chord_steps_set = set(chord_steps)
            matching_scales = {}
            for scale_name, scale_steps in self.scales.all.items():

                scale_steps_set = set(scale_steps)
                if chord_steps_set.intersection(scale_steps_set) == chord_steps_set:
                    matching_scales.update({scale_name: scale_steps})

            full_dict.update(
                {chord_name: {"steps": chord_steps, "matching_scales": matching_scales}})

        return full_dict

    def __scales_chords(self) -> dict:

        full_dict = {}

        for scale_name, scale_steps in self.scales.all.items():
            scale_steps_set = set(scale_steps)
            matching_chords = {}
            for chord_name, chord_steps in self.chords.all.items():

                chord_steps_set = set(chord_steps)
                if chord_steps_set.intersection(scale_steps_set) == chord_steps_set:
                    matching_chords.update({chord_name: chord_steps})

            full_dict.update(
                {scale_name: {"steps": scale_steps, "matching_chords": matching_chords}})

        return full_dict
