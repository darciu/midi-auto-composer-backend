import os
from enum import Enum
import subprocess

from midi2audio import FluidSynth


class Difficulty(str, Enum):
    ionian = "easy"
    harmonic_minor = "normal"
    melodic_minor = "hard"

class Tonation(str, Enum):
    c = "c"
    c_sharp = "c#"
    d = "d"
    d_sharp = "d#"
    e = "e"
    f = "f"
    f_sharp = "f#"
    g = "g"
    g_sharp = "g#"
    a = "a"
    a_sharp = "a#"
    b = "b"
    random = "random"


def remove_file(path: str) -> None:

    os.remove(path)
    


def convert_midi_file(path: str) -> str:
    
    fs = FluidSynth(sound_font='soundfonts/arachno.sf2')
    new_path = path[:-3] + 'wav'
    subprocess.run(['fluidsynth', '-ni', '-g', '3', 'soundfonts/arachno.sf2', path, '-F', new_path])
    # fs.midi_to_audio(path, new_path)
    os.remove(path)

    return new_path

