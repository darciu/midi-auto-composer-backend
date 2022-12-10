"""
plik ten daje dostęp do wybranej harmonii, w formie listy
harmonia powstaje po podaniu tonacji (jej kolejne stopnie okeślane są jako tuplety tonacja, rodzaj akordu)
harmonia moze być modyfikowana po jej wywołaniu:
 - mozna podnosić/obnizać jej stopnie o podany interwał (max to odległość do sąsiadujacego stopnia)
 - mozna zmieniać typ akordu na danym stopniu

 więc zwracany jest obiekt per dana harmonia, którą trzeba podać jako parametr w wywoływaniu instancji


"""
import json
from dataclasses import dataclass
from typing import List, Tuple

# na podstawie podanego dźwięku i interwału mozna uzyskać kolejny dźwięk
# bierz dźwięk początkowy
# bierz interwał
# odległość pomiędzy dźwiękami za pomocą indexu


@dataclass
class Harmony:
    harmony_chords: List[Tuple(str, str)]

    @staticmethod
    def create_harmony(harmony_name: str, tonal_key: str) -> "Harmony":

        with open('static/harmonies.json', 'r') as handler:
            harmony = json.load(handler)[harmony_name]
        
        progression = harmony["progression"]
        steps = harmony["steps"]

        def add_interval(tonal_key, interval):
            tones = [
            'c',
            'c#',
            'd',
            'd#',
            'e',
            'f',
            'f#',
            'g',
            'g#',
            'a',
            'a#',
            'b'
        ]
            # zamienić tonacje flat na sharp
            if tonal_key not in tonal_key:
                raise ValueError(f'There is no such a tone: {tonal_key}')
            idx = tones.index(tonal_key)
            if idx + interval > 11:
                return tones[idx + interval - 12]
            elif idx + interval < 0:
                return tones[idx + interval + 12]
            else:
                return tones[idx + interval]

        harmony_chords = []
        for chord, interval in zip(progression, steps):
            harmony_chords.append((chord, add_interval(tonal_key, interval)))

        return Harmony(harmony_chords)


    
        





        

