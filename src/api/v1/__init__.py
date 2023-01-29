import os
from midi2audio import FluidSynth

def remove_file(path: str) -> None:

    os.remove(path)
    


def convert_midi_file(path: str) -> str:
    
    fs = FluidSynth(sound_font='soundfonts/arachno.sf2')
    new_path = path[:-3] + 'wav'
    fs.midi_to_audio(path, new_path)
    os.remove(path)

    return new_path

