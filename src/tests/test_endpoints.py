from itertools import combinations
from fastapi.testclient import TestClient
import pytest

from main import app
from entities.chords import Chords

@pytest.fixture
def scales():
    return Scales.load()

@pytest.fixture
def chords():
    return Chords.load()

client = TestClient(app)


# POST ENDPOINTS

def test_multiple_scales_multiple_chords_response():
    response = client.post('v1/multiple_scales_multiple_chords', json = {"repeat_n_times":1})
    assert response.status_code == 200
 
def test_one_scale_one_chord_response():
    response = client.post('v1/one_scale_one_chord', json = {"repeat_n_times":1})
    assert response.status_code == 200

def test_pattern_response():
    response = client.post('v1/pattern', json = {"preview_pattern":False, "pause_between":False})
    assert response.status_code == 200


def test_random_background_chords_response():
    response = client.post('v1/random_background_chords', json = {"repeat_n_times":1})
    assert response.status_code == 200

def test_random_scales_one_chord_response():
    response = client.post('v1/random_scales_one_chord', json = {"repeat_n_times":1})
    assert response.status_code == 200


# GET ENDPOINTS

## CHORDS

def test_chord_by_name(chords):
    for chord_name in chords.all.keys():
        response = client.get(f'v1/chords/chord_by_name/{chord_name}')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_all_chords_names_response():
    response = client.get('v1/chords/all_chords_names')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


param_input_filter_chords = combinations(['major', 'minor', 'dimished_fifth', 'perfect_fifth', 'augmented_fifth', 'minor_seventh', 'major_seventh'], 2)

@pytest.mark.parametrize("pairs", param_input_filter_chords)
def test_filter_chords(pairs):
    response = client.get(f'v1/chords/filter_chords/?chords_types={pairs[0]}&chords_types={pairs[1]}')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
