import random
import math
import numpy as np
from typing import Tuple, List, Optional

from midiutil import MIDIFile

from entities.chords import Chords
from entities.scales import Scales
from entities.move_scale import MoveScale
from entities.structures import all_melodies


chords = Chords.load()
scales = Scales.load()

class MIDIComposer:
    def __init__(self, tempo: int, notes_range: tuple, move_scale_max: int = 2, difficulty: str = 'normal'):
        """This class allows create midi files for different instruments parts (melody, backing chords, bass, percussion) 

        Attributes
        ----------
        tempo: int
            Recording tempo.
        time_pointer: int
            Indicates where actual beat time is.
        notes_range: tuple
            What is the range of notes that melody can be played.
        move_scale_max: int
            Maximum step while playing melody within particular scale.
        difficulty: str
            Probability of choosing closer of further scale steps.
        """
        self.tempo = tempo
        self.time_pointer = 0
        self.time_finish = 0
        self.notes_range = notes_range
        self.move_scale_max = move_scale_max
        self.difficulty = difficulty
        self.MIDIobj = MIDIFile(1)
        self.MIDIobj.addTempo(0, 0, tempo) # track, time, tempo
        self.tone_start: dict = {
                                    'c':48,
                                    'c#':49,
                                    'd':50,
                                    'd#':51,
                                    'e':40,
                                    'f':41,
                                    'f#':42,
                                    'g':43,
                                    'g#':44,
                                    'a':45,
                                    'a#':46,
                                    'b':47,
                                }
        
        self.intervals_map: dict = {
                                    'm2':1,
                                    'M2':2,
                                    'm3':3,
                                    'M3':4,
                                    'P4':5,
                                    'TT':6,
                                    'P5':7,
                                    'm6':8,
                                    'M6':9,
                                    'm7':10,
                                    'M7':11,
                                    'P8':12
        }

    # USEFUL FUNCTIONS

    def get_tonation(self, tonation: str) -> str:
        """if tone_key value is random, randomly pick from all keys list"""

        if tonation not in ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b','random']:
            raise ValueError(f'Not invalid tone key ({tonation})!')
        elif tonation == 'random':
            return random.choice(list(self.tone_start.keys()))
        else:
            return tonation
        
    def timeout_to_n_repeats(self, timeout: int, quarternotes: int, sequence_len: int = 1) -> int:

        return int((self.tempo/(quarternotes*sequence_len))*(timeout/60))
    

    def get_time_duration(self) -> int:
        "time duration of MIDI in seconds"
        # timeout = quarternotes/(tempo/60)
        return int(math.ceil(self.time_finish/(self.tempo/60)))
        
        
    def midi_to_file(self, filepath: str):
        with open(filepath, "wb") as output_file:
            self.MIDIobj.writeFile(output_file)

    def close_midi(self):
        self.MIDIobj.close()

    def __find_random_notes(self, scale_name: str, scale_tonation: str, note_pitch: int, shift_note_index: Optional[int],
                            count_notes: int):

        move_scale_obj = MoveScale(self.move_scale_max, self.difficulty)
        
        scale_sequence = scales.detailed.get(scale_name)['steps']
        
        tonal_scale, primes = self.__create_tonal_scale_and_primes_lists(scale_sequence, scale_tonation, self.notes_range)
        
        
        if note_pitch == None:
            # first random note choosen from primes
            note_pitch = random.choice(primes)
            
        elif note_pitch not in tonal_scale:
            # most similar pitch to previous note pitch
            note_pitch = min(tonal_scale, key=lambda x: abs(x-note_pitch))
           
        list_of_notes = []
        
        for _ in range(count_notes):

            # find new note pitch and what kind of shift it was
            note_pitch, shift_note_index = move_scale_obj.find_new_note(
                shift_note_index, tonal_scale, note_pitch)

            list_of_notes.append(note_pitch)

        # return shift_note_index in order to know what was the last shift of the note
        return list_of_notes, shift_note_index
    
    def __create_tonal_scale_and_primes_lists(self, scale: list, scale_tonation: str, notes_range: tuple) -> Tuple[list, list]:
        """return list of tonal scale with all notes and also primes pitches within range of notes"""

        min_notes_range = notes_range[0]
        max_notes_range = notes_range[1]
        primes = list(range(self.tone_start[scale_tonation],max_notes_range+1,12))
        all_tones = [prime + tone for tone in scale for prime in primes]
        all_tones = [x for x in all_tones if x <= max_notes_range and x >= min_notes_range]
        
        return sorted(all_tones), sorted(primes)
    
    # INTERVALS

    def add_intervals_melody_part(self, intervals: List[str], program: int, timeout: int):
        """Add random melody part
        
        Parameters
        ----------
        intervals: List[str]
            List of possible intervals to be played.
        program: int
            Instrument program number.
        """
        
        note = random.choice(list(range(46, 64)))

        repeat_n_times = self.timeout_to_n_repeats(timeout,1)

        # track = 0
        # channel = 0
        
        time = self.time_pointer
        self.MIDIobj.addProgramChange(0, 0, 0, program)
        
        volume = 0.8

        self.MIDIobj.addNote(0, 0, note, time, 1, int(volume*127)) # track, channel, pitch, time, duration, volume

        low_range = self.notes_range[0]
        high_range = self.notes_range[1]

        if self.difficulty == 'easy':
            weights = [1/elem for elem in range(1,len(intervals)+1)]
        elif self.difficulty == 'normal':
            weights = list(np.ones(len(intervals),dtype=int))
        elif self.difficulty == 'hard':
            weights = list(range(1,len(intervals)+1))

        intervals = sorted(intervals, key=lambda d: self.intervals_map[d])

        for time in range(1, repeat_n_times+1):
            
            interval = self.intervals_map.get(random.choices(intervals,k=1,weights=weights)[0])
            add_operator = random.choice([False,True])

            if add_operator:
                if note + interval <= high_range:
                    note += interval
                else:
                    note -= interval
            else:
                if note - interval >= low_range:
                    note -= interval
                else:
                    note += interval

            self.MIDIobj.addNote(0, 0, note, time, 1, int(volume*127)) # track, channel, pitch, time, duration, volume

        if time > self.time_finish:
            self.time_finish = time

        
    # SINGLE MELODY
    
    def add_random_melody_part(self, scales: List[tuple], quarternotes_measures: List[int], program: int, volume: float):
        """Add random melody part
        
        Parameters
        ----------
        scales: List[tuple]
            List of tuples containing scales names and their tonations.
        program: int
            Instrument program number.
        """
        # track = 0
        # channel = 0
        
        time = self.time_pointer
        self.MIDIobj.addProgramChange(0, 0, 0, program)
        
        note_pitch = None
        
        for (scale_name, scale_tonation), quarternotes in zip(scales,quarternotes_measures):
            
            for measure_type in ['call','response']:
                if measure_type == 'call':

                    if scale_name is None:
                        time += quarternotes
                    else:
                        note_pitch = self.__add_single_measure_random_melody(scale_name, scale_tonation, note_pitch, time, quarternotes, volume)
                        
                        time += quarternotes

                elif measure_type == 'response':
                    time += quarternotes

        if time > self.time_finish:
            self.time_finish = time

    def add_scale_pattern_part(self, pattern: List[int], scale_name: str, tonation: str, play_upwards: bool
                               , preview_pattern: bool, pause_between: bool = True):
        """Add random melody part
        
        Parameters
        ----------
        pattern: List[int]
            Pattern steps.
        scale_name: str
            Scale name.
        tonation: str
            Scale's tonation.
        play_upwards: bool
            Should pattern be played upwards or downwards.
        preview_pattern: bool
            Play pattern preview.
        pause_between: bool
            There is always one quarternote pause added between pattern played. 
        """
        self.MIDIobj.addProgramChange(0, 0, 0, 1)

        scale_sequence = scales.detailed.get(scale_name)['steps']
        
        tonal_scale, _ = self.__create_tonal_scale_and_primes_lists(scale_sequence, tonation, self.notes_range)

        if play_upwards:
            
            if preview_pattern:
                self.pattern_preview(tonal_scale, pattern)
            
            time = self.time_pointer

            for tonal_scale_step in tonal_scale:

                if not tonal_scale.index(tonal_scale_step) + max(pattern) >= len(tonal_scale) + 1:

                    for pattern_step in pattern:

                        note_index = tonal_scale.index(tonal_scale_step) + pattern_step -1

                        self.MIDIobj.addNote(0, 0, tonal_scale[note_index], time, 1, int(1*127))
                        time += 1
                    if pause_between:
                        time += 1

            self.MIDIobj.addNote(0, 0, tonal_scale[-1], time, 1, int(1*127))
            
        else:
            
            tonal_scale_reversed = list(reversed(tonal_scale))

            pattern = list(reversed(pattern))
            
            if preview_pattern:
                self.pattern_preview(tonal_scale_reversed, pattern)
            
            time = self.time_pointer
            
            for tonal_scale_step in tonal_scale_reversed:
                
                if not tonal_scale_reversed.index(tonal_scale_step) + max(pattern) -1 >= len(tonal_scale_reversed):
                    
                    for pattern_step in pattern:
                        
                        note_index = tonal_scale_reversed.index(tonal_scale_step) + pattern_step -1
                        
                        self.MIDIobj.addNote(0, 0, tonal_scale_reversed[note_index], time, 1, int(1*127))
                        time += 1
                    if pause_between:
                        time += 1
                        
            self.MIDIobj.addNote(0, 0, tonal_scale_reversed[-1], time, 1, int(1*127))
        
        if time > self.time_finish:
            self.time_finish = time


    def pattern_preview(self, tonal_scale: list, pattern: list):
        """Play pattern preview based on scale in certain tonation and the pattern to be played
        
        Parameters
        ----------
        tonal_scale: list
            Generated scale pitches within certain tonation.
        pattern: list
            Pattern to be played.
        """
        
        time = self.time_pointer

        for i in range(len(pattern)):
            
            self.MIDIobj.addNote(0, 0, tonal_scale[pattern[i]-1], time, 1, int(1*127))
            
            time += 1
        
        self.time_pointer = time + 3 # wait three beats
            
    def __add_single_measure_random_melody(self, scale_name: str, scale_tonation: str, prev_note_pitch: Optional[int], 
                                           time: int, quarternotes: int, volume: float):
        

        rhythm = self.__get_rhythm(quarternotes, [0.25,0.5,1,1.5,2], [0.1,1.2,1,0.2,0.2])

        
        notes, _ = self.__find_random_notes(scale_name, scale_tonation, prev_note_pitch, None, len(rhythm))
        
        last_note_pitch = notes[-1]
        
        
        for note, single_rhythm in zip(notes, rhythm):

            self.MIDIobj.addNote(0, 0, note, time, single_rhythm, int(volume*127)) # track, channel, pitch, time, duration, volume
            time = time + single_rhythm
        
        return last_note_pitch
    
        
    # BACKGROUND CHORDS
    
    def add_background_chords_part(self, chords: List[tuple], quarternotes_measures: List[int], program: int, volume: float):
        """Add background chords part. Every first beat is different than the next ones.
        
        Parameters
        ----------
        chords: List[tuple]
            Tuples containing chords names and their tonations.
        program: int
            Instrument program number.
        """

        # track = 0
        # channel = 1
        
        time = self.time_pointer
        self.MIDIobj.addProgramChange(0, 1, time, program)
        
        for (chord_name, chord_tonation), quarternotes in zip(chords,quarternotes_measures):
            for _ in range(2):
                self.__add_single_chord(chord_name, chord_tonation, quarternotes, time, volume)
                time += quarternotes

        if time > self.time_finish:
            self.time_finish = time
            
    def __add_single_chord(self, chord_name, chord_tonation, quarternotes, time, volume):
        
        chord_sequence = chords.detailed.get(chord_name)['steps']
        
        tonal_chord, _ = self.__create_tonal_scale_and_primes_lists(chord_sequence, chord_tonation, self.notes_range)
        
        # chord in two first octaves
        chord_sequence = [tone for tone in tonal_chord if tone <= tonal_chord[0]+24 and tone > tonal_chord[0]]
        
        # add first chord's quarternote
        
        rhythm = self.__get_rhythm(quarternotes, [1,2], [3,2])
                
        self.__add_chords_first_beat(chord_sequence, time, volume + 0.1, rhythm[0])
        
        time += rhythm[0]
        
        
        for rhythm_value in rhythm[1:]:
            
            self.__add_chords_next_beat(chord_sequence, time, volume, rhythm_value)
            
            time += rhythm_value

    
    def __add_chords_first_beat(self, chord_sequence, time, volume, rhythm_value):
        
        if random.choice([1,2,3,4]) in [1,2,3]:
        
            notes = [chord_sequence[0]] + chord_sequence[2:4]
        else:
            notes = [chord_sequence[0]] + chord_sequence[2:3]
                
        self.__arpeggio_chord(notes, time, volume, rhythm_value)
            
    def __add_chords_next_beat(self, chord_sequence, time, volume, rhythm_value):
        
        rn = random.choices([1,2,3,4], k=1, weights=[2,3,3,1])[0]
        if rn == 1:
            # three notes, one quarter note
            notes = random.sample(chord_sequence, k=3)
            volume += random.choice([-0.025,0,0.025])
            self.__arpeggio_chord(notes, time, volume, rhythm_value)
            
        elif rn == 2:
            # two notes, one quarter note
            notes = random.sample(chord_sequence, k=2)
            volume += random.choice([-0.025,0,0.025])
            self.__arpeggio_chord(notes, time, volume, rhythm_value)
            
        elif rn == 3:
            # two eighth notes, ascending
            notes = sorted(random.sample(chord_sequence, k=2))
            volume += random.choice([-0.025,0,0.025])
            note1 = [notes[0]]
            note2 = [notes[1]]
            self.__arpeggio_chord(note1, time, volume, 1)
            self.__arpeggio_chord(note2, time + 0.5, volume, 1)
            
        elif rn == 4:
            pass
        
            
    def __arpeggio_chord(self, notes: list, time: int, volume: int, rhythm_value):
        """Play chord with little delays"""
        volume += random.choice([-0.05,0,0.05])
        for note in notes:
            self.MIDIobj.addNote(0, 1, note, time, rhythm_value, int(volume*127))
            time += random.randrange(10)/300
            
    
    # BASSLINE
    
    def add_bassline_part(self, chords, quarternotes_measures: int, program: int, volume: float):
        """Add bassline part based on given chords.
        
        Parameters
        ----------
        chords: tuple
            Tuples containing chords names and their tonations.
        program: int
            Instrument program number.
        """
        # track = 0
        # channel = 2
        
        time = self.time_pointer
        self.MIDIobj.addProgramChange(0, 2, time, program)
        
        
        for (chord_name, chord_tonation), quarternotes in zip(chords,quarternotes_measures):
            for _ in range(2):
                self.__add_single_bassline(chord_name, chord_tonation, quarternotes, time, volume)
                time += quarternotes

        if time > self.time_finish:
            self.time_finish = time
            
    def __add_single_bassline(self, chord_name, chord_tonation, quarternotes, time, volume):
        
        chord_sequence = chords.detailed.get(chord_name)['steps']
        
        tonal_chord, _ = self.__create_tonal_scale_and_primes_lists(chord_sequence, chord_tonation, self.notes_range)
        
        chord_sequence = [tone for tone in tonal_chord if tone <= tonal_chord[0]+12 and tone > tonal_chord[0]]
        
        rhythm = self.__get_rhythm(quarternotes, [0.5,1,2], [0.7,1,3])
                
        
        # first quarternote
        
        note = random.choices([chord_sequence[0],chord_sequence[2]], k=1, weights=[5,2])[0]

        volume += random.choice([-0.05,0,0.05])
        
        self.MIDIobj.addNote(0, 2, note-12, time, rhythm[0], int(volume*127))
        
        time += rhythm[0]
                
        # other notes
        for rhythm_value in rhythm[1:]:
            
            note = random.choice(chord_sequence[1:])

            volume += random.choice([-0.1,-0.05,0])

            self.MIDIobj.addNote(0, 2, note-12, time, rhythm_value, int(volume*127))
            
            time += rhythm_value
    
    def __get_rhythm(self, quarternotes: int, possible_rhythms: list = [1,2], rhythms_weights: list = [1,1]):
        rhythm_sum = 0
        rhythm = []
        while rhythm_sum != quarternotes:
            num = random.choices(possible_rhythms, k=1, weights=rhythms_weights)[0]
            if rhythm_sum + num <= quarternotes:
                rhythm_sum += num
                rhythm.append(num)
        return rhythm


    # PERCUSSION
            
    def add_percussion_part(self, quarternotes_measures: int, volume: float):
        """Add percussion part based on quarternotes per measure. In MIDI channel 9 is dedicated for percussion.
        
        Parameters
        ----------
        n_measures: int
            How many measures to repeat.
        """
        # track = 0
        # channel = 9

        # 35 - kick
        # 38 - snare
        # 42 - closed hi hat
        # 46 - open hi hat

        def get_volume(possible_volumes: list) -> int:
            return int(random.choice(possible_volumes)*127)
        
        time = self.time_pointer
        
        for quarternotes in quarternotes_measures:
            for _ in range(2):

                if quarternotes == 2:
                    chance = random.randrange(0,6)

                    if chance in [0,1,2,3,4]:

                        hh_volume = random.choice([0.4,0.5])

                        self.MIDIobj.addNote(0,9,35,time, 1,65)
                        self.MIDIobj.addNote(0,9,42,time+1, 1,int(hh_volume*127))

                        chance_inner = random.choice([0,1,2,3,4])
                        if  chance_inner == 0:
                            self.MIDIobj.addNote(0,9,random.choice([42,46]),time+1.5, 1,30)
                        elif chance_inner in [1,2]:
                            self.MIDIobj.addNote(0,9,35,time+1.5, 1,45)
                        else:
                            pass

                    elif chance in [5]:
                        #double kick

                        hh_volume = random.choice([0.35,0.4,0.5])

                        self.MIDIobj.addNote(0,9,35,time, 1,40)
                        self.MIDIobj.addNote(0,9,35,time+0.5, 1,65)
                        self.MIDIobj.addNote(0,9,42,time+1, 1,int(hh_volume*127))

                        self.MIDIobj.addNote(0,9,random.choice([42,42,46]),time+1.5, 1,int(random.choice([0,0.4,0.45])*127))


                    time += 2


                elif quarternotes == 3:

                    
                    self.MIDIobj.addNote(0,9,35,time, 1,65)
                    self.MIDIobj.addNote(0,9,42,time+1, 1,55)
                    chance = random.randrange(0,7)
                    
                    if chance in [0,1,2]:         
                        if random.choice([0,1,2,3]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+2, 1,45)
                        else:
                            self.MIDIobj.addNote(0,9,42,time+2, 1,45)
                    elif chance in [3,4,5]:
                        self.MIDIobj.addNote(0,9,42,time+2, 1,55)
                        if random.choice([0,1,2,3,4]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+2.5, 1,40)
                        else:
                            self.MIDIobj.addNote(0,9,35,time+2.5, 1,45)
                    elif chance in [6]:
                        self.MIDIobj.addNote(0,9,35,time+1.66, 1,55)
                        if random.choice([0,1,2,3]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+2, 1,45)
                        else:
                            self.MIDIobj.addNote(0,9,42,time+2, 1,45)
                    

                    time +=3




                elif quarternotes == 4:

                    self.MIDIobj.addNote(0,9,35,time, 1,get_volume([0.6,0.7]))
                    self.MIDIobj.addNote(0,9,42,time+1, 1,get_volume([0.45,0.5]))
                    self.MIDIobj.addNote(0,9,35,time+2, 1,get_volume([0.5,0.55]))
                    if random.choice([0,1,2,3,4]) == 0:
                        self.MIDIobj.addNote(0,9,35,time+2.5, 1,get_volume([0.45,0.5]))

                    self.MIDIobj.addNote(0,9,random.choice([42,42,42,46]),time+3, 1,get_volume([0.4,0.45,0.5]))

                    time += 4


                elif quarternotes == 5:
                    self.MIDIobj.addNote(0,9,35,time, 1,get_volume([0.6,0.7]))
                    self.MIDIobj.addNote(0,9,42,time+1, 1,get_volume([0.45,0.5]))
                    self.MIDIobj.addNote(0,9,35,time+2, 1,get_volume([0.5,0.55]))
                    if random.choice([0,1,2,3,4]) == 0:
                        self.MIDIobj.addNote(0,9,35,time+2.5, 1,get_volume([0.45,0.5]))

                    self.MIDIobj.addNote(0,9,42,time+5, 1,get_volume([0,0,0.4,0.45,]))

                    self.MIDIobj.addNote(0,9,random.choice([42,42,42,46]),time+4, 1,get_volume([0.4,0.45,0.5]))

                    time += 5

                elif quarternotes == 6:


                    self.MIDIobj.addNote(0,9,35,time, 1,65)
                    self.MIDIobj.addNote(0,9,42,time+1, 1,55)
                    chance = random.randrange(0,7)
                    
                    if chance in [0,1,2]:         
                        if random.choice([0,1,2,3]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+2, 1,45)
                        else:
                            self.MIDIobj.addNote(0,9,42,time+2, 1,45)
                    elif chance in [3,4,5]:
                        self.MIDIobj.addNote(0,9,42,time+2, 1,55)
                        if random.choice([0,1,2,3,4]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+2.5, 1,40)
                        else:
                            self.MIDIobj.addNote(0,9,35,time+2.5, 1,45)
                    elif chance in [6]:
                        self.MIDIobj.addNote(0,9,35,time+1.66, 1,55)
                        if random.choice([0,1,2,3]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+2, 1,45)
                        else:
                            self.MIDIobj.addNote(0,9,42,time+2, 1,45)

                    self.MIDIobj.addNote(0,9,35,time+3, 1,65)
                    self.MIDIobj.addNote(0,9,42,time+4, 1,55)


                    chance = random.randrange(0,7)
                    
                    if chance in [0,1,2]:         
                        if random.choice([0,1,2,3]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+5, 1,45)
                        else:
                            self.MIDIobj.addNote(0,9,42,time+5, 1,45)
                    elif chance in [3,4,5]:
                        self.MIDIobj.addNote(0,9,42,time+5, 1,55)
                        if random.choice([0,1,2,3,4]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+5.5, 1,40)
                        else:
                            self.MIDIobj.addNote(0,9,35,time+5.5, 1,45)
                    elif chance in [6]:
                        self.MIDIobj.addNote(0,9,35,time+4.66, 1,55)
                        if random.choice([0,1,2,3]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+5, 1,45)
                        else:
                            self.MIDIobj.addNote(0,9,42,time+5, 1,45)

                    time += 6

                elif quarternotes == 7:
                    
                    self.MIDIobj.addNote(0,9,35,time, 1,get_volume([0.6,0.7]))
                    self.MIDIobj.addNote(0,9,42,time+1, 1,get_volume([0.45,0.5]))
                    self.MIDIobj.addNote(0,9,35,time+2, 1,get_volume([0.5,0.55]))
                    if random.choice([0,1,2,3,4]) == 0:
                        self.MIDIobj.addNote(0,9,35,time+2.5, 1,get_volume([0.45,0.5]))

                    self.MIDIobj.addNote(0,9,random.choice([42,42,42,46]),time+3, 1,get_volume([0.4,0.45,0.5]))

                    self.MIDIobj.addNote(0,9,35,time+4, 1,65)
                    self.MIDIobj.addNote(0,9,42,time+5, 1,55)
                    chance = random.randrange(0,7)
                    
                    if chance in [0,1,2]:         
                        if random.choice([0,1,2,3]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+6, 1,45)
                        else:
                            self.MIDIobj.addNote(0,9,42,time+6, 1,45)
                    elif chance in [3,4,5]:
                        self.MIDIobj.addNote(0,9,42,time+6, 1,55)
                        if random.choice([0,1,2,3,4]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+6.5, 1,40)
                        else:
                            self.MIDIobj.addNote(0,9,35,time+6.5, 1,45)
                    elif chance in [6]:
                        self.MIDIobj.addNote(0,9,35,time+5.66, 1,55)
                        if random.choice([0,1,2,3]) == 0:
                            self.MIDIobj.addNote(0,9,46,time+6, 1,45)
                        else:
                            self.MIDIobj.addNote(0,9,42,time+6, 1,45)
                    

                    time +=7

                if time > self.time_finish:
                    self.time_finish = time


    def add_melody(self, tonation: str, melody_id: str):
        
        # pitch, time, volume
        key = self.tone_start[tonation] + 12
        
        melody = all_melodies.get(melody_id)

        volume = 0.8
        time = self.time_pointer        

        for pitch, duration in melody['notes']:

            self.MIDIobj.addNote(0, 0, pitch + key, time, 1, int(volume*127)) # track, channel, pitch, time, duration, volume
            time += duration

        if time > self.time_finish:
            self.time_finish = time

        
        
        # for note in test_melody:
        #     pitch = self.tone_start[tonation] + note[0]
        #     time = note[1]
        #     volume = note[2]

        #     self.MIDIobj.addNote(0, 0, random.randint(40,50), time, 1, int(volume*127)) # track, channel, pitch, time, duration, volume

