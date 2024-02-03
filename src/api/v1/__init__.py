import os
import subprocess

from pydub import AudioSegment
from pydub.silence import split_on_silence


def remove_file(path: str) -> None:

    os.remove(path)
    
def convert_midi_file(path: str, time_duration: int, bitrate: str = '44100') -> str:
    
    wav_path = path.replace('.mid','.wav')
    mp3_path = path.replace('.mid','.mp3')
    subprocess.run(['fluidsynth', '-ni', '-g', '1', 'soundfonts/arachno.sf2', path, '-F', wav_path, '-r', bitrate])
    audio = AudioSegment.from_wav(wav_path)
    audio = audio[:time_duration*1000]
    audio.export(mp3_path, format='mp3')
    os.remove(path)
    os.remove(wav_path)



