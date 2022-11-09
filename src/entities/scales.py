import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Scales:
    modal_by_name: Dict[dict]
    modal_by_order : Dict[dict]
    seven_tone: dict
    six_tone: dict
    pentatonic: dict
    other: dict
    all: dict

    # modal:nazwa_modalna:nazwa

    @staticmethod
    def load_scales(path) -> "Scales":

        def shift_scale(scale, n = 0):
            nth_elem = scale[n]
            return sorted([elem + 12 if elem < 0 else elem for elem in [elem-nth_elem for elem in scale]])


        modal_by_name = {}
        modal_by_order = {}
        seven_tone = {}
        six_tone = {}
        pentatonic = {}
        all = {}

        scales = json.loads(path)

        # Modal part
        modal_scales = scales['modal_scales']

        for name, struct in modal_scales.items():
            steps = list(map(int, struct['steps'].split(',')))
            modal_names = [name] + struct['other_modal_names'].split(',')

            temp_by_name = {}
            temp_by_order = {}
            for i in range(len(steps)):
                
                temp_by_name.update({modal_names[i]:shift_scale(steps, n=i)})
                temp_by_order.update({i+1:{'name':modal_names[i],'scale':shift_scale(steps, n=i)}})

                if modal_names[i] in all.keys():
                    raise NameError('Two scales with the same names')
                    
                all.update({modal_names[i]:shift_scale(steps, n=i)})

            modal_by_name.update({name:temp_by_name})
            modal_by_order.update({name:temp_by_order})

            if len(steps) == 7:
                seven_tone.update({name:temp_by_name})
            elif len(steps) == 6:
                six_tone.update({name:temp_by_name})
            elif len(steps) == 5:
                pentatonic.update({name:temp_by_name})

        # Other part

        other_scales = scales['other_scales']

        all.update(other_scales)


        



        
