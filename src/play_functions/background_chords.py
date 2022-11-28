import scamp
import random

def play_background_chord(instrument: scamp.instruments.ScampInstrument, quarternotes: int, tonal_chord: list, volume: float):





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

















    # tonal_chord_wo_prime = [elem for elem in tonal_chord if elem%tonal_chord[0] != 0]
    # pool1 = []
    # pool1.append([tonal_chord[0],tonal_chord[2]])
    # pool1.append([tonal_chord[0],tonal_chord[2]])
    # pool1.append([tonal_chord[0]])
    # pool1.append([tonal_chord[0],tonal_chord[1], tonal_chord[2]])


    
    # pool2 = []
    # pool2.append(random.choices(tonal_chord_wo_prime,k=2))
    # pool2.append(random.choices(tonal_chord_wo_prime,k=2))
    # pool2.append(random.choices(tonal_chord_wo_prime,k=1))
    # pool2.append(random.choices(tonal_chord_wo_prime,k=1))

    

    # # kolejne dźwięki powinny być bliej siebie


    # for _ in range(quarternotes):

    #     time_left = 2

    #     duration = np.random.choice([1,0.5], p=[1/2,1/2])
    #     time_left -= duration
    #     instrument.play_chord(random.choice(pool1),0.2,duration)
    #     while time_left > 0:
    #         duration = np.random.choice([1,0.5], p=[3/4,1/4])
            
    #         if time_left - duration >= 0:
    #             time_left -= duration
    #             instrument.play_chord(random.choice(pool2),0.2,duration)
    #         else:
    #             pass
                

                


