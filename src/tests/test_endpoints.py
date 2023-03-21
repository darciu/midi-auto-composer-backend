from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

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