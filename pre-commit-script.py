import json
import sys
sys.path.append(".")

from src.entities.scales import Scales
from src.entities.chords import Chords

scales = Scales.load()
chords = Chords.load()

scales_detailed = []

for elem in scales.all:
   temp = scales.get_details(elem)
   value = elem
   steps = temp[elem].get('steps')
   alias_eng = temp[elem].get('alias_eng')
   alias_pl = temp[elem].get('alias_pl')

   scales_detailed.append({"steps":steps
            ,"alias_eng":alias_eng
            ,"alias_pl":alias_pl
            ,"value":value})
   



scales_tree = []
modals = scales.modals
for elem in modals.keys():
    value = elem
    subscales = modals[elem]
    scales_tree.append({"subscales":subscales
                        ,"value":value})
    


scales_tree.append({"subscales":scales.six_tone
                ,"value":"six tone"})




chords_detailed = []

for elem in chords.all:
   temp = chords.get_details(elem)
   value = elem
   steps = temp[elem].get('steps')
   alias_eng = temp[elem].get('alias_eng')
   alias_notation = temp[elem].get('alias_notation')

   chords_detailed.append({"steps":steps
            ,"alias_eng":alias_eng
            ,"alias_notation":alias_notation
            ,"value":value})
   




chords_tree = []

chords_tree.append({"subchords":chords.major
                    ,"value":"major"})

chords_tree.append({"subchords":chords.minor
                    ,"value":"minor"})

chords_tree.append({"subchords":chords.perfect_fifth
                    ,"value":"perfect_fifth"})

chords_tree.append({"subchords":chords.dimished_fifth
                    ,"value":"dimished_fifth"})

chords_tree.append({"subchords":chords.augmented_fifth
                    ,"value":"augmented_fifth"})

chords_tree.append({"subchords":chords.minor_seventh
                    ,"value":"minor_seventh"})

chords_tree.append({"subchords":chords.major_seventh
                    ,"value":"major_seventh"})



with open("pre-commit-output/scales_detailed.json", "w") as f: 
    json.dump(scales_detailed, f)

with open("pre-commit-output/scales_tree.json", "w") as f: 
    json.dump(scales_tree, f)

with open("pre-commit-output/chords_detailed.json", "w") as f: 
    json.dump(chords_detailed, f)

with open("pre-commit-output/chords_tree.json", "w") as f: 
    json.dump(chords_tree, f)