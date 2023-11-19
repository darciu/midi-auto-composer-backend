import os
import subprocess

from midi2audio import FluidSynth
from pydub import AudioSegment





def remove_file(path: str) -> None:

    os.remove(path)
    


def convert_midi_file(path: str) -> str:
    
    wav_path = path.replace('.mid','.wav')
    mp3_path = path.replace('.mid','.mp3')
    subprocess.run(['fluidsynth', '-ni', '-g', '3', 'soundfonts/arachno.sf2', path, '-F', wav_path, '-r','22050'])
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format='mp3')
    os.remove(path)
    os.remove(wav_path)
    return mp3_path



