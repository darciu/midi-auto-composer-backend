import scamp
import random
import numpy as np

def play_background_chords(instrument: scamp.instruments.ScampInstrument, quarternotes: int, tonal_chord: list):


    tonal_chord_wo_prime = [elem for elem in tonal_chord if elem%tonal_chord[0] != 0]
    pool1 = []
    pool1.append([tonal_chord[0],tonal_chord[2]])
    pool1.append([tonal_chord[0],tonal_chord[2]])
    pool1.append([tonal_chord[0]])
    pool1.append([tonal_chord[0],tonal_chord[1], tonal_chord[2]])


    
    pool2 = []
    pool2.append(random.choices(tonal_chord_wo_prime,k=2))
    pool2.append(random.choices(tonal_chord_wo_prime,k=2))
    pool2.append(random.choices(tonal_chord_wo_prime,k=1))
    pool2.append(random.choices(tonal_chord_wo_prime,k=1))

    




    for _ in range(quarternotes):

        time_left = 2

        duration = np.random.choice([1,0.5], p=[1/2,1/2])
        time_left -= duration
        instrument.play_chord(random.choice(pool1),0.2,duration)
        while time_left > 0:
            duration = np.random.choice([1,0.5], p=[3/4,1/4])
            
            if time_left - duration >= 0:
                time_left -= duration
                instrument.play_chord(random.choice(pool2),0.2,duration)
            else:
                pass
                

                


