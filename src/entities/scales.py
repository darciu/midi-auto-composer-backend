from dataclasses import dataclass
from typing import Dict, Union

from .structures import all_scales

@dataclass
class Scales:
    modal_by_name: Dict[str,list]
    modal_by_order : Dict[int,Dict[str,Union[str,list]]]
    seven_tone: Dict[str,list]
    six_tone: Dict[str,list]
    pentatonic: Dict[str,list]
    all: Dict[str,list]


    @staticmethod
    def load() -> "Scales":
        """Create Scales class object from static dictionary"""

        def shift_scale(scale, n = 0):
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
            steps = list(map(int, struct['steps'].split(',')))
            modal_names = [name] + struct['other_modal_names'].split(',')

            temp_by_name = {}
            temp_by_order = {}

            # iteracja po kolejnych stopniach
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
            try:
                steps_ = list(map(int, steps.split(',')))
            except:
                raise ValueError(steps)

            if len(steps_) == 7:
                seven_tone.update({name:steps_})
            elif len(steps_) == 6:
                six_tone.update({name:steps_})
            elif len(steps_) == 5:
                pentatonic.update({name:steps_})
                
            all.update({name:steps_})


        return Scales(modal_by_name, modal_by_order, seven_tone, six_tone, pentatonic, all)




        



        
