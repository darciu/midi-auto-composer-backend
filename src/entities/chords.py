from dataclasses import dataclass
from typing import Dict, List, Union
from .structures import all_chords



@dataclass
class Chords:
    """A class holding chords lists and detailed object with little more details about these chords

    Attributes
    -----------
    all: list
        all chords stored as list
    minor: list
        minor third chords stored as list
    major: list
        major third chords stored as list
    dimished_fifth: list
        dimished_fifth third chords stored as list
    perfect_fifth: list
        perfect_fifth third chords stored as list
    augmented_fifth: list
        augmented_fifth third chords stored as list
    minor_seventh: list
        minor_seventh third chords stored as list
    major_seventh: list
        major_seventh third chords stored as list
    """
    all: List[str]
    minor: List[str]
    major: List[str]
    dimished_fifth: List[str]
    perfect_fifth: List[str]
    augmented_fifth: List[str]
    minor_seventh: List[str]
    major_seventh: List[str]
    detailed: Dict[str, dict]

    @staticmethod
    def load() -> "Chords":
        """Create Chords class object from static dictionary"""

        all = [name for name in all_chords.keys()]
        minor = [name for name, struct in all_chords.items() if 3 in struct["steps"]]
        major = [name for name, struct in all_chords.items() if 4 in struct["steps"]]
        dimished_fifth = [name for name, struct in all_chords.items() if 6 in struct["steps"]]
        perfect_fifth = [name for name, struct in all_chords.items() if 7 in struct["steps"]]
        augmented_fifth = [name for name, struct in all_chords.items() if 8 in struct["steps"]]
        minor_seventh = [name for name, struct in all_chords.items() if 10 in struct["steps"]]
        major_seventh = [name for name, struct in all_chords.items() if 11 in struct["steps"]]

        detailed = {name:{"steps":struct["steps"], "alias_eng":struct["alias_eng"], "alias_notation":struct["alias_notation"]} for name, struct in all_chords.items()}

        return Chords(all, minor, major, dimished_fifth, perfect_fifth, augmented_fifth, minor_seventh, major_seventh, detailed)

    def filter_chords(self, filters: Union[List[str], list]) -> List[str]:
        """
        Select chords by providing filters list (eg. minor, major)
        
        Parameters
        ----------
        filters : List[str]
            List of strings of chords types. Available chord types: major, minor, dimished_fifth, perfect_fifth,
            augmented_fifth, minor_seventh, major_seventh.
        """

        filters_dict = {'minor':self.minor
            ,'major':self.major
            ,'dimished_fifth':self.dimished_fifth
            ,'perfect_fifth':self.perfect_fifth
            ,'augmented_fifth':self.augmented_fifth
            ,'minor_seventh':self.minor_seventh
            ,'major_seventh':self.major_seventh}
        filtered_chords = self.all.copy()
        for fltr in filters:
            filtered_chords = [name for name in filtered_chords if name in filters_dict[fltr]]
        return filtered_chords

    def get_details(self, names:Union[str, list]) -> Dict[str, dict]:
        """
        Get details about chords providing chords name(s)

        Parameters
        ----------
        names: Union[str, list]
            List of string names (or single string name)
        """
        if isinstance(names, str):
            names = [names]
        
        return {k:v for k,v in self.detailed.items() if k in names}