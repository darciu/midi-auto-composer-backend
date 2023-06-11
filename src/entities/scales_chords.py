from dataclasses import dataclass, field
from entities.scales import Scales
from entities.chords import Chords


@dataclass
class ScalesChords:
    """A class combining Scales and Chords classes also providing dictionaries which scales
    matches to particular chord and vice versa, what chords matches to particular scale

    Attributes
    ----------
    scales: entities.scales.Scales
        A Scales class object.
    chords: entities.chords.Chords
        A Chords class object.
    chord_scales: dict
        A dictionary containing every chord with all scales matching it.
    scale_chords: dict
        A dictionary containing every scale with all chords matching it.
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

        for chord_name, chord_struct in self.chords.detailed.items():
            chord_steps_set = set(chord_struct["steps"])
            matching_scales = []
            for scale_name, scale_struct in self.scales.detailed.items():

                scale_steps_set = set(scale_struct["steps"])
                if chord_steps_set.intersection(scale_steps_set) == chord_steps_set:
                    matching_scales.append(scale_name)

            full_dict.update(
                {chord_name: {"steps": chord_struct["steps"], "matching_scales": self.scales.get_details(matching_scales)}})

        return full_dict

    def __scales_chords(self) -> dict:

        full_dict = {}

        for scale_name, scale_struct in self.scales.detailed.items():
            scale_steps_set = set(scale_struct["steps"])
            matching_chords = []
            for chord_name, chord_struct in self.chords.detailed.items():

                chord_steps_set = set(chord_struct["steps"])
                if chord_steps_set.intersection(scale_steps_set) == chord_steps_set:
                    matching_chords.append(chord_name)

            full_dict.update(
                {scale_name: {"steps": scale_struct["steps"], "matching_chords": self.chords.get_details(matching_chords)}})

        return full_dict
