from itertools import combinations
import urllib.parse
from fastapi.testclient import TestClient
import pytest

from main import app
from entities.chords import Chords
from entities.scales import Scales

@pytest.fixture
def scales():
    return Scales.load()

@pytest.fixture
def chords():
    return Chords.load()

client = TestClient(app)


# POST ENDPOINTS

def test_pattern_response():
    response = client.post('v1/pattern')
    assert response.status_code == 200


def test_custom_creator():
    response = client.post('v1/custom_creator')
    assert response.status_code == 200
 
def test_one_scale_one_chord_response():
    response = client.post('v1/one_scale_one_chord')
    assert response.status_code == 200




def test_random_scales_one_chord_response():
    response = client.post('v1/random_scales_one_chord')
    assert response.status_code == 200


# GET ENDPOINTS

## SCALES

def test_scale_by_name(scales):
    for scale_name in scales.detailed.keys():
        scale_name = urllib.parse.quote_plus(scale_name)
        response = client.get(f'v1/scales/scale_by_name/{scale_name}')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)


def test_all_scales_names_response():
    response = client.get('v1/scales/all_scales')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_all_scales_n_tones():
    for n_tones in ['seven_tone','six_tone','pentatonic']:
        response = client.get(f'v1/scales/{n_tones}')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert len(response.json()) > 0 


def test_all_modal_names_response():
    response = client.get('v1/scales/all_modals_names')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_modal_sub_scales():
    for modal_name in ['ionian', 'harmonic_minor', 'melodic_minor', 'harmonic_major', 'double_harmonic_major', 'pentatonic_major']:
        response = client.get(f'v1/scales/modal_sub_scales/{modal_name}')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert len(response.json()) > 0 


## CHORDS

def test_chord_by_name(chords):
    for chord_name in chords.detailed.keys():
        response = client.get(f'v1/chords/chord_by_name/{chord_name}')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

def test_all_chords_names_response():
    response = client.get('v1/chords/all_chords')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


param_input_filter_chords = combinations(['major', 'minor', 'dimished_fifth', 'perfect_fifth', 'augmented_fifth', 'minor_seventh', 'major_seventh'], 2)

@pytest.mark.parametrize("pairs", param_input_filter_chords)
def test_filter_chords(pairs):
    response = client.get(f'v1/chords/filter_chords/?chords_types={pairs[0]}&chords_types={pairs[1]}')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


## SCALES CHORDS

def test_scales_matching_chord(chords):
    for chord_name in chords.detailed.keys():
        response = client.get(f'v1/scales_chords/scales_matching_chord/{chord_name}')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)


def test_chords_matching_scale(scales):
    for scale_name in scales.detailed.keys():
        scale_name = urllib.parse.quote_plus(scale_name)
        response = client.get(f'v1/scales_chords/chords_matching_scale/{scale_name}')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)