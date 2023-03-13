import random
from midiutil import MIDIFile

from entities.chords import Chords
from entities.scales import Scales
from entities.move_scale import MoveScale
from play_functions.helper_functions import create_tonal_scale_and_primes_lists


# zamienić quarternotes na metrum, które będzie też zawierało łatwe do wydobycia wartości ćwierćnut
# dodać kolejne bicia perkusyjne
# sparametryzować volume dla każdego z kanałów
# dodać wybór instrumentów
# dodać metrodę obliczającą timeout w taktach

chords = Chords.load()
scales = Scales.load()

class MIDIComposer:
    def __init__(self, tempo, quarternotes, notes_range, move_scale_max = 2, difficulty = 'normal'):
        self.tempo = tempo
        self.time_pointer = 0
        self.quarternotes = quarternotes
        self.notes_range = notes_range
        self.move_scale_max = move_scale_max
        self.difficulty = difficulty
        self.MIDIobj = MIDIFile(1)
        self.MIDIobj.addTempo(0, 0, tempo) # track, time, tempo
        
    
    def add_random_melody_part(self, scales, program):
        # track = 0
        # channel = 0
        
        time = self.time_pointer
        self.MIDIobj.addProgramChange(0, 0, 0, program)
        
        note_pitch = None
        
        for scale_name, scale_tonation in scales:
            
            note_pitch = self.add_single_measure_random_melody(scale_name, scale_tonation, note_pitch, time)
            
            time += self.quarternotes
            
    def add_single_measure_random_melody(self, scale_name, scale_tonation, prev_note_pitch, time):
        
        
        notes, _ = self.find_random_notes(scale_name, scale_tonation, prev_note_pitch, None)
        
        last_note_pitch = notes[-1]
        
        volume = 0.7
        
        for note in notes:
            self.MIDIobj.addNote(0, 0, note, time, 1, int(volume*127)) # track, channel, pitch, time, duration, volume
            time = time + 1
        
        return last_note_pitch
    
    
    def find_random_notes(self, scale_name, scale_tonation, note_pitch, shift_note_index):
        
        move_scale_obj = MoveScale(self.move_scale_max, self.difficulty)
        
        scale_sequence = scales.all.get(scale_name)
        
        tonal_scale, primes = create_tonal_scale_and_primes_lists(scale_sequence, scale_tonation, self.notes_range)
        
        
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

        
        
        
    # BACKGROUND CHORDS
    
    def add_background_chords_part(self, chords, program):
        # track = 0
        # channel = 1
        
        time = self.time_pointer
        self.MIDIobj.addProgramChange(0, 1, time, program)
        
        for chord_name, chord_tonation in chords:
            self.add_single_chord(chord_name, chord_tonation, time)
            time += self.quarternotes
            
    def add_single_chord(self, chord_name, chord_tonation, time):
        
        
        chord_sequence = chords.all.get(chord_name)
        
        tonal_chord, _ = create_tonal_scale_and_primes_lists(chord_sequence, chord_tonation, self.notes_range)
        
        # chord in two first octaves
        chord_sequence = [tone for tone in tonal_chord if tone <= tonal_chord[0]+24 and tone > tonal_chord[0]]
        
        # add first chord's quarternote
        
        rhythm = self.get_rhythm([1,2],[3,2])
                
        self.add_chords_first_beat(chord_sequence, time, 0.5, rhythm[0])
        
        time += rhythm[0]
        
        
        for rhythm_value in rhythm[1:]:
            
            self.add_chords_next_beat(chord_sequence, time, 0.4, rhythm_value)
            
            time += rhythm_value

    
    def add_chords_first_beat(self, chord_sequence, time, volume, rhythm_value):
        
        if random.choice([1,2,3,4]) in [1,2,3]:
        
            notes = [chord_sequence[0]] + chord_sequence[2:4]
        else:
            notes = [chord_sequence[0]] + chord_sequence[2:3]
                
        self.arpeggio_chord(notes, time, volume, rhythm_value)
            
    def add_chords_next_beat(self, chord_sequence, time, volume, rhythm_value):
        
        rn = random.choices([1,2,3,4], k=1, weights=[2,3,3,1])[0]
        if rn == 1:
            # three notes, one quarter note
            notes = random.sample(chord_sequence, k=3)
            self.arpeggio_chord(notes, time, volume, rhythm_value)
            
        elif rn == 2:
            # two notes, one quarter note
            notes = random.sample(chord_sequence, k=2)
            self.arpeggio_chord(notes, time, volume, rhythm_value)
            
        elif rn == 3:
            # two eighth notes, ascending
            notes = sorted(random.sample(chord_sequence, k=2))
            note1 = [notes[0]]
            note2 = [notes[1]]
            self.arpeggio_chord(note1, time, volume, 1)
            self.arpeggio_chord(note2, time + 0.5, volume, 1)
            
        elif rn == 4:
            pass
        
            
    def arpeggio_chord(self, notes: list, time: int, volume: int, rhythm_value):
        for note in notes:
            self.MIDIobj.addNote(0, 1, note, time, rhythm_value, int(volume*127))
            time += random.randrange(10)/300
            
        
    
    # BASSLINE
    
    def add_bassline_part(self, chords, program):
        # track = 0
        # channel = 2
        
        time = self.time_pointer
        self.MIDIobj.addProgramChange(0, 2, time, program)
        
        
        for chord_name, chord_tonation in chords:
            self.add_single_bassline(chord_name, chord_tonation, time)
            time += self.quarternotes
            
    def add_single_bassline(self, chord_name, chord_tonation, time):
        
        
    
        chord_sequence = chords.all.get(chord_name)
        
        tonal_chord, _ = create_tonal_scale_and_primes_lists(chord_sequence, chord_tonation, self.notes_range)
        
        chord_sequence = [tone for tone in tonal_chord if tone <= tonal_chord[0]+12 and tone > tonal_chord[0]]
        
        rhythm = self.get_rhythm([1,2,4],[1,3,6])
                
        
        # first note
        
        note = random.choices([chord_sequence[0],chord_sequence[2],chord_sequence[0]+12], k=1, weights=[5,2,1])[0]
        
        self.MIDIobj.addNote(0, 2, note-12, time, rhythm[0], int(0.5*127))
        
        time += rhythm[0]
                
        # other notes
        for rhythm_value in rhythm[1:]:
            
            note = random.choice(chord_sequence[1:])

            self.MIDIobj.addNote(0, 2, note-12, time, 4, int(0.45*127))
            
            time += rhythm_value
                        
        
            
    def add_percussion_part(self, n_measures):
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
        
            
    def get_rhythm(self, possible_rhythms = [1,2], rhythms_weights = [1,1]):
        rhythm_sum = 0
        rhythm = []
        while rhythm_sum != self.quarternotes:
            num = random.choices(possible_rhythms, k=1, weights=rhythms_weights)[0]
            if rhythm_sum + num <= self.quarternotes:
                rhythm_sum += num
                rhythm.append(num)
        return rhythm
    
    def timeout_to_n_repeats(self, tempo: int, timeout: int) -> int:

        return int((tempo/self.quarternotes)*(timeout/60))
            
    def midi_to_file(self, filepath: str):
        with open(filepath, "wb") as output_file:
            self.MIDIobj.writeFile(output_file)

    def close_midi(self):
        self.MIDIobj.close()