import random
from typing import Tuple, List, Optional

from midiutil import MIDIFile


from entities.chords import Chords
from entities.scales import Scales
from entities.move_scale import MoveScale


# zamienić quarternotes na metrum, które będzie też zawierało łatwe do wydobycia wartości ćwierćnut
# dodać kolejne bicia perkusyjne
# sparametryzować volume dla każdego z kanałów
# dodać wybór instrumentów
# dodać metrodę obliczającą timeout w taktach

chords = Chords.load()
scales = Scales.load()

class MIDIComposer:
    def __init__(self, tempo: int, quarternotes: int, notes_range: tuple, move_scale_max: int = 2, difficulty: str = 'normal'):
        """This class allows create midi files for different instruments parts (melody, backing chords, bass, percussion) 

        Attributes
        ----------
        tempo: int
            Recording tempo.
        time_pointer: int
            Indicates where actual beat time is.
        quarternotes: int
            How many quarternotes per one measure.
        notes_range: tuple
            What is the range of notes that melody can be played.
        move_scale_max: int
            Maximum step while playing melody within particular scale.
        difficulty: str
            Probability of choosing closer of further scale steps.
        """
        self.tempo = tempo
        self.time_pointer = 0
        self.quarternotes = quarternotes
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

    # USEFUL FUNCTIONS

    def get_tonation(self, tonation: str) -> str:
        """if tone_key value is random, randomly pick from all keys list"""

        if tonation not in ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b','random']:
            raise ValueError(f'Not invalid tone key ({tonation})!')
        elif tonation == 'random':
            return random.choice(list(self.tone_start.keys()))
        else:
            return tonation
        
    def timeout_to_n_repeats(self, timeout: int, sequence_len: int = 1) -> int:

        return int((self.tempo/(self.quarternotes*sequence_len))*(timeout/60))
            
    def midi_to_file(self, filepath: str):
        with open(filepath, "wb") as output_file:
            self.MIDIobj.writeFile(output_file)

    def close_midi(self):
        self.MIDIobj.close()

    def __find_random_notes(self, scale_name: str, scale_tonation: str, note_pitch: int, shift_note_index: Optional[int]):
        
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
        
        for _ in range(self.quarternotes):

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
        
    # SINGLE MELODY
    
    def add_random_melody_part(self, scales: List[tuple], program: int):
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
        
        for scale_name, scale_tonation in scales:
            
            note_pitch = self.__add_single_measure_random_melody(scale_name, scale_tonation, note_pitch, time)
            
            time += self.quarternotes

    def add_scale_pattern_part(self, pattern: List[int], scale_name: str, tonation: str, play_upwards: bool, preview_pattern: bool, pause_between: bool = True):
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

                        self.MIDIobj.addNote(0, 1, tonal_scale[note_index], time, 1, int(1*127))
                        time += 1
                    if pause_between:
                        time += 1

            self.MIDIobj.addNote(0, 1, tonal_scale[-1], time, 1, int(1*127))
            
        else:
            
            tonal_scale_reversed = list(reversed(tonal_scale))
            
            if preview_pattern:
                self.pattern_preview(tonal_scale_reversed, pattern)
            
            time = self.time_pointer
            
            for tonal_scale_step in tonal_scale_reversed:
                
                if not tonal_scale_reversed.index(tonal_scale_step) + max(pattern) -1 >= len(tonal_scale_reversed):
                    
                    for pattern_step in pattern:
                        
                        note_index = tonal_scale_reversed.index(tonal_scale_step) + pattern_step -1
                        
                        self.MIDIobj.addNote(0, 1, tonal_scale_reversed[note_index], time, 1, int(1*127))
                        time += 1
                    if pause_between:
                        time += 1
                        
            self.MIDIobj.addNote(0, 1, tonal_scale_reversed[-1], time, 1, int(1*127))


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
            
    def __add_single_measure_random_melody(self, scale_name: str, scale_tonation: str, prev_note_pitch: Optional[int], time):
        
        
        notes, _ = self.__find_random_notes(scale_name, scale_tonation, prev_note_pitch, None)
        
        last_note_pitch = notes[-1]
        
        volume = 0.7
        
        for note in notes:
            self.MIDIobj.addNote(0, 0, note, time, 1, int(volume*127)) # track, channel, pitch, time, duration, volume
            time = time + 1
        
        return last_note_pitch
    
        
    # BACKGROUND CHORDS
    
    def add_background_chords_part(self, chords: List[tuple], program: int):
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
        
        for chord_name, chord_tonation in chords:
            self.__add_single_chord(chord_name, chord_tonation, time)
            time += self.quarternotes
            
    def __add_single_chord(self, chord_name, chord_tonation, time):
        
        
        chord_sequence = chords.detailed.get(chord_name)['steps']
        
        tonal_chord, _ = self.__create_tonal_scale_and_primes_lists(chord_sequence, chord_tonation, self.notes_range)
        
        # chord in two first octaves
        chord_sequence = [tone for tone in tonal_chord if tone <= tonal_chord[0]+24 and tone > tonal_chord[0]]
        
        # add first chord's quarternote
        
        rhythm = self.__get_rhythm([1,2],[3,2])
                
        self.__add_chords_first_beat(chord_sequence, time, 0.5, rhythm[0])
        
        time += rhythm[0]
        
        
        for rhythm_value in rhythm[1:]:
            
            self.__add_chords_next_beat(chord_sequence, time, 0.4, rhythm_value)
            
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
            self.__arpeggio_chord(notes, time, volume, rhythm_value)
            
        elif rn == 2:
            # two notes, one quarter note
            notes = random.sample(chord_sequence, k=2)
            self.__arpeggio_chord(notes, time, volume, rhythm_value)
            
        elif rn == 3:
            # two eighth notes, ascending
            notes = sorted(random.sample(chord_sequence, k=2))
            note1 = [notes[0]]
            note2 = [notes[1]]
            self.__arpeggio_chord(note1, time, volume, 1)
            self.__arpeggio_chord(note2, time + 0.5, volume, 1)
            
        elif rn == 4:
            pass
        
            
    def __arpeggio_chord(self, notes: list, time: int, volume: int, rhythm_value):
        """Play chord with little delays"""
        for note in notes:
            self.MIDIobj.addNote(0, 1, note, time, rhythm_value, int(volume*127))
            time += random.randrange(10)/300
            
    
    # BASSLINE
    
    def add_bassline_part(self, chords, program):
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
        
        
        for chord_name, chord_tonation in chords:
            self.__add_single_bassline(chord_name, chord_tonation, time)
            time += self.quarternotes
            
    def __add_single_bassline(self, chord_name, chord_tonation, time):
        
        chord_sequence = chords.detailed.get(chord_name)['steps']
        
        tonal_chord, _ = self.__create_tonal_scale_and_primes_lists(chord_sequence, chord_tonation, self.notes_range)
        
        chord_sequence = [tone for tone in tonal_chord if tone <= tonal_chord[0]+12 and tone > tonal_chord[0]]
        
        rhythm = self.__get_rhythm([1,2,4],[1,3,6])
                
        
        # first quarternote
        
        note = random.choices([chord_sequence[0],chord_sequence[2],chord_sequence[0]+12], k=1, weights=[5,2,1])[0]
        
        self.MIDIobj.addNote(0, 2, note-12, time, rhythm[0], int(0.5*127))
        
        time += rhythm[0]
                
        # other notes
        for rhythm_value in rhythm[1:]:
            
            note = random.choice(chord_sequence[1:])

            self.MIDIobj.addNote(0, 2, note-12, time, 4, int(0.45*127))
            
            time += rhythm_value
    
    def __get_rhythm(self, possible_rhythms: list = [1,2], rhythms_weights: list = [1,1]):
        rhythm_sum = 0
        rhythm = []
        while rhythm_sum != self.quarternotes:
            num = random.choices(possible_rhythms, k=1, weights=rhythms_weights)[0]
            if rhythm_sum + num <= self.quarternotes:
                rhythm_sum += num
                rhythm.append(num)
        return rhythm


    # PERCUSSION
            
    def add_percussion_part(self, n_measures: int):
        """Add percussion part based on quarternotes per measure. In MIDI channel 9 is dedicated for percussion.
        
        Parameters
        ----------
        n_measures: int
            How many measures to repeat.
        """
        # track = 0
        # channel = 9
        
        time = self.time_pointer
        
        for _ in range(n_measures):
            self.MIDIobj.addNote(0,9,35,time, 2,65)
            self.MIDIobj.addNote(0,9,40,time+2, 2,60)
            
            self.MIDIobj.addNote(0,9,42,time, 2,65)
            self.MIDIobj.addNote(0,9,42,time+1, 2,65)
            self.MIDIobj.addNote(0,9,42,time+2, 2,55)
            self.MIDIobj.addNote(0,9,42,time+3, 2,65)
            time += 4
