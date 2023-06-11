from dataclasses import dataclass
from typing import Dict, Union, List

from .structures import all_scales

@dataclass
class Scales:
    """A class holding scales lists and detailed object with little more details about these scales

    Attributes
    ----------
    modals: dict
        Dictionary where keys are modal names (first scale name) and values are lists of other sub-modal scales names.
    seven_tone: list
        List of all seven tone scales.
    six_tone: list
        List of all six tone scales.
    pentatonic: list
        List of all five tone scales.
    all: list
        List of all scales.
    detailed: dict
        For given scale name see details like scale steps, scale aliases.
    """
    modals: Dict[str,list]
    seven_tone: List[str]
    six_tone: List[str]
    pentatonic: List[str]
    all: List[str]
    detailed: Dict[str, dict]


    @staticmethod
    def load() -> "Scales":
        """Create Scales class object from static dictionary"""

        def shift_scale(scale: list, n = 0) -> List[int]:
            """Shift modal scale by n steps"""

            nth_elem = scale[n]
            return sorted([elem + 12 if elem < 0 else elem for elem in [elem-nth_elem for elem in scale]])

        modals = {}
        seven_tone = []
        six_tone = []
        pentatonic = []
        all = []
        detailed = {}


        # Modal part
        modal_scales = all_scales['modal_scales']

        for name, struct in modal_scales.items():
            steps = struct['steps']
            modal_names = [name] + struct['other_modal_names'].split(',')
            aliases_eng = struct['aliases_eng'].split(',')
            aliases_pl = struct['aliases_pl'].split(',')

            modals.update({name:[name] + struct['other_modal_names'].split(',')})

            # iterate following scale steps
            for i in range(len(steps)):

                if modal_names[i] in detailed.keys():
                    raise NameError(f'Two scales with the same name! {modal_names[i]}')
                
                detailed.update({modal_names[i]:{"steps":shift_scale(steps, n=i)
                                                 ,"alias_eng":aliases_eng[i]
                                                 ,"alias_pl":aliases_pl[i]}})

                if len(steps) == 7:
                    seven_tone.append(modal_names[i])
                elif len(steps) == 6:
                    six_tone.append(modal_names[i])
                elif len(steps) == 5:
                    pentatonic.append(modal_names[i])

                all.append(modal_names[i])

        # Other part

        other_scales = all_scales['other_scales']

        for name, struct in other_scales.items():

            steps = struct['steps']
            alias_eng = struct['alias_eng']
            alias_pl = struct['alias_pl']

            if len(steps) == 7:
                seven_tone.append(name)
            elif len(steps) == 6:
                six_tone.append(name)
            elif len(steps) == 5:
                pentatonic.append(name)
                
            all.append(name)

            detailed.update({name:{"steps":steps
                                ,"alias_eng":alias_eng
                                ,"alias_pl":alias_pl}})

        return Scales(modals, seven_tone, six_tone, pentatonic, all, detailed)
    
    def get_details(self, names:Union[str, list]) -> Dict[str, dict]:
        """
        Get details about scales providing chords name(s)

        Parameters
        ----------
        names: Union[str, list]
            List of string names (or single string name)
        """
        if isinstance(names, str):
            names = [names]
        
        return {k:v for k,v in self.detailed.items() if k in names}

