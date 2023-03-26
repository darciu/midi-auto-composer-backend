import pytest
from entities.midi_composer import MIDIComposer

@pytest.fixture
def midi_obj():
    return MIDIComposer(120,4,(40,80))


def test_add_random_melody_part(midi_obj):

    scales_input = [('ionian','c')]

    midi_obj.add_random_melody_part(scales_input,42)

    
def test_add_scale_pattern_part(midi_obj):

    pattern = [1,2,4]
    scale_name = 'ionian'
    tonation = 'c'
    play_upwards = True
    preview_pattern = True

    midi_obj.add_scale_pattern_part(pattern, scale_name, tonation, play_upwards, preview_pattern)

def test_pattern_preview(midi_obj):

    scale_sequence = [0,3,9]
    tonation = 'c'
    pattern = [1,2,4]
    tonal_scale, _ = midi_obj._MIDIComposer__create_tonal_scale_and_primes_lists(scale_sequence, tonation, midi_obj.notes_range)

    midi_obj.pattern_preview(tonal_scale, pattern)


def test_add_background_chords_part(midi_obj):

    chords_input = [('major','c')]

    midi_obj.add_background_chords_part(chords_input, 12)

def test_add_bassline_part(midi_obj):

    chords_input = [('major','c')]

    midi_obj.add_bassline_part(chords_input, 12)


def test_add_percussion_part(midi_obj):

    midi_obj.add_percussion_part(4)


def test_get_tonation(midi_obj):

    tonation = midi_obj.get_tonation('random')

    assert tonation in ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']

def test_timeout_to_n_repeats(midi_obj):

    assert midi_obj.timeout_to_n_repeats(10) == 5
    assert midi_obj.timeout_to_n_repeats(60) == 30
    assert midi_obj.timeout_to_n_repeats(90) == 45

def test_close_midi(midi_obj):
    midi_obj.close_midi()
