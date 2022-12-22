from scamp.instruments import ScampInstrument
import random

from play_functions.helper_functions import create_tonal_scale_and_primes_lists, get_tone_key

# przenieść tutaj wytwarzanie tonal_chord

def play_background_chord(instrument: ScampInstrument, quarternotes: int, chord: str, chord_tonation: str, notes_range: tuple, volume: float = 0.4) -> None:
    """
    Play background chord

        Parameters:
            instrument (ScampInstrument): An instance of ScampInstrument class
            quarternotes (int): how many beats per measure there will be
            tonal_chord (list): list of integers with given chord pitches according to exact tonation
            volume (float): volume of playing background chord; ranges from 0 to 1

    """

    chord_tonation = get_tone_key(chord_tonation)

    tonal_chord, _ = create_tonal_scale_and_primes_lists(
        chord, chord_tonation, notes_range)

    chord = [tone for tone in tonal_chord if tone <= tonal_chord[0]+24 and tone > tonal_chord[0]]


    if random.choice([1,2,3,4]) in [1,2,3]:
        instrument.play_chord([tonal_chord[0]] + tonal_chord[2:4],volume+0.2,2)
    else:
        instrument.play_chord([tonal_chord[0]] + [tonal_chord[2:3]],volume+0.1,2)
    for _ in range(quarternotes-1):
        rn = random.choice([1,2,3,4,5,6,7,8,9])
        if rn in [1,2,3]:
            instrument.play_chord(random.choices(chord, k=3),volume-0.1,1)
            instrument.play_chord(random.choices(chord, k=1),volume,1)
        elif rn == 4:
            instrument.play_chord(random.choices(chord, k=3),volume,1)
            instrument.play_chord(random.choices(chord, k=1),volume,0.5)
            instrument.play_chord(random.choices(chord, k=1),volume,0.5)
        else:

            instrument.play_chord(random.choices(chord, k=3),volume-0.1,2)
