import pytest
from entities.midi_composer import MIDIComposer

@pytest.fixture
def midi_obj():
    return MIDIComposer(120,4,(40,80))



