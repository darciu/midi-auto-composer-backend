from dataclasses import dataclass
from entities.scales import Scales
from entities.chords import Chords

@dataclass
class ScalesChords:

    scales: Scales
    chords: None
    chords_scales: None
    scales_chords: None



    scales = Scales.load_scales('static/scales.json')

    @staticmethod
    def create_object():
        scales = Scales.load_scales('static/scales.json')

        chords = Chords.load_chords('static/chords.json')




# {
#     "nazwa_akordu": {
#         "stopnie": [],
#         "pasujące_skale": {
#             "skala1": []
#             ,"skala2":[]
#         }
#     }
# }

# ### druga wersja

# {"skala":{"stopnie":[]
#         ,"pasujące_akordy":{
#             "akord1":[],
#             "akord2":[]
#         }}}