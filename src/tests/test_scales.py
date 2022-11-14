import sys
import os
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from entities.scales import Scales

scales = Scales.load_scales('static/scales.json')


scales_list = "ionian,dorian,phrygian,lydian,mixolydian,aeolian,locrian".split(',')
             
 
@pytest.mark.parametrize("modal_scale", scales_list)
def test_scales(modal_scale):
    assert modal_scale in scales.seven_tone.keys()
    assert modal_scale in scales.modal_by_name['ionian'].keys()
    