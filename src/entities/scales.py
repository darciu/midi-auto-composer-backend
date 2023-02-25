from dataclasses import dataclass
from typing import Dict, Union, List

from .structures import all_scales

@dataclass
class Scales:
    """A class holding scales in dictionaries in form:
    chord type (str) : list of integer steps

    where steps are following building scale pitches
    eg. "ionian": [0,2,4,5,7,9,11]

    Attributes
    -----------
    modal_by_name: dict
        Dictionary where keys are modal names and values are dictionaries with sub-modal name: steps.
    seven_tone: dict
        Dictionary storing all seven tone scales with corresponding scale steps.
    six_tone: dict
        Dictionary storing all six tone scales with corresponding scale steps.
    pentatonic: dict
        Dictionary storing all five tone scales with corresponding scale steps.
    all: dict
        Dictionary storing all scales with corresponding scale steps.
    """
    modal_by_name: Dict[str,list]
    modal_by_order : Dict[int,Dict[str,Union[str,list]]]
    seven_tone: Dict[str, List[int]]
    six_tone: Dict[str, List[int]]
    pentatonic: Dict[str, List[int]]
    all: Dict[str, List[int]]


    @staticmethod
    def load() -> "Scales":
        """Create Scales class object from static dictionary"""

        def shift_scale(scale: list, n = 0) -> List[int]:
            """shift modal scale by n steps"""

            nth_elem = scale[n]
            return sorted([elem + 12 if elem < 0 else elem for elem in [elem-nth_elem for elem in scale]])

        modal_by_name = {}
        modal_by_order = {}
        seven_tone = {}
        six_tone = {}
        pentatonic = {}
        all = {}


        # Modal part
        modal_scales = all_scales['modal_scales']

        for name, struct in modal_scales.items():
            steps = struct['steps']
            modal_names = [name] + struct['other_modal_names'].split(',')

            temp_by_name = {}
            temp_by_order = {}

            # iterate following scale steps
            for i in range(len(steps)):

                if modal_names[i] in all.keys():
                    raise NameError(f'Two scales with the same name! {modal_names[i]}')
                
                temp_by_name.update({modal_names[i]:shift_scale(steps, n=i)})
                temp_by_order.update({i+1:{'name':modal_names[i],'scale':shift_scale(steps, n=i)}})

                if len(steps) == 7:
                    seven_tone.update({modal_names[i]:shift_scale(steps, n=i)})
                elif len(steps) == 6:
                    six_tone.update({modal_names[i]:shift_scale(steps, n=i)})
                elif len(steps) == 5:
                    pentatonic.update({modal_names[i]:shift_scale(steps, n=i)})

                all.update({modal_names[i]:shift_scale(steps, n=i)})

            modal_by_name.update({name:temp_by_name})
            modal_by_order.update({name:temp_by_order})

        # Other part

        other_scales = all_scales['other_scales']

        for name, steps in other_scales.items():
            

            if len(steps) == 7:
                seven_tone.update({name:steps})
            elif len(steps) == 6:
                six_tone.update({name:steps})
            elif len(steps) == 5:
                pentatonic.update({name:steps})
                
            all.update({name:steps})


        return Scales(modal_by_name, modal_by_order, seven_tone, six_tone, pentatonic, all)

