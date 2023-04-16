import sys
import os
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from entities.scales import Scales

@pytest.fixture
def scales():
    return Scales.load()


ionian_modal = "ionian,dorian,phrygian,lydian,mixolydian,aeolian,locrian"
harmonic_minor = "harmonic_minor,locrian_13,ionian_#5,dorian_#11,phrygian_dominant,lydian_#9,harmonic_dimished"
melodic_minor = "melodic_minor,dorian_b9,lydian_augmented,lydian_dominant,mixolydian_b13,locrian_9,superlocrian"

param_input = []
param_input.append(('ionian', ionian_modal))
param_input.append(('harmonic_minor', harmonic_minor))
param_input.append(('melodic_minor', melodic_minor))
             
print(param_input)
 
@pytest.mark.parametrize("modal_name, modal_scales", param_input)
def test_modal_scales(scales, modal_name, modal_scales):
    for scale in modal_scales.split(','):
        assert scale in scales.modal_by_name[modal_name].keys()



def test_non_existing_scale(scales):
    with pytest.raises(Exception):
        scales.all['unknown']