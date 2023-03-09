import random
from midiutil import MIDIFile

from entities.chords import Chords
from play_functions.helper_functions import create_tonal_scale_and_primes_lists

chords = Chords.load()

# zamienić quarternotes na metrum, które będzie też zawierało łatwe do wydobycia wartości ćwierćnut
# dodać kolejne bicia perkusyjne

class MIDIComposer:
    def __init__(self, tempo, quarternotes, notes_range):
        self.tempo = tempo
        self.time_pointer = 0
        self.quarternotes = quarternotes
        self.notes_range = notes_range
        self.MIDIobj = MIDIFile(1)
        self.MIDIobj.addTempo(0, 0, tempo) # track, time, tempo
        
    def add_melody_part(self, notes: list, volume: int, program: int):
        # track = 0
        # channel = 1
        
        time = self.time_pointer
        self.MIDIobj.addProgramChange(0, 0, 0, program)
        
        for note in notes:
            self.MIDIobj.addNote(0, 0, note, time, 1, int(volume*127)) # track, channel, pitch, time, duration, volume
            time = time + 1
    
        
    # BACKGROUND CHORDS
    
    def add_background_chords_part(self, chords, program):
        # track = 0
        # channel = 1
        
        time = self.time_pointer
        self.MIDIobj.addProgramChange(0, 2, time, program)
        
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
            self.MIDIobj.addNote(0, 0, note, time, rhythm_value, int(volume*127))
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
                        

    # PERCUSSION
            
    def add_percussion_part(self, n_measures):
        # track = 0
        # channel = 9
        
        time = self.time_pointer
        
        for i in range(n_measures):
            
            if self.quarternotes == 3:
                self.add_single_percussion_three_quarter(time, i%2==0)
            elif self.quarternotes == 4:
                self.add_single_percussion_four_quarter(time, i%2==0)

            time += self.quarternotes
    
    def add_single_percussion_three_quarter(self, time, measure_is_even: bool):
        
        if measure_is_even:
            # kick
            self.MIDIobj.addNote(0,9,35,time, 2,65)

            # hi-hat
            self.MIDIobj.addNote(0,9,42,time+1, 2,65)
            self.MIDIobj.addNote(0,9,42,time+2, 2,65)

        else:
            # snare
            self.MIDIobj.addNote(0,9,40,time, 2,60)

            # hi-hat
            self.MIDIobj.addNote(0,9,42,time+1, 2,65)
            self.MIDIobj.addNote(0,9,42,time+2, 2,65)
            

    def add_single_percussion_four_quarter(self, time, measure_is_even: bool):
        
        if measure_is_even:

            # kick
            self.MIDIobj.addNote(0,9,35,time, 2,65)

            # snare
            self.MIDIobj.addNote(0,9,40,time+2, 2,60)

            # hi-hat
            self.MIDIobj.addNote(0,9,42,time, 2,65)
            self.MIDIobj.addNote(0,9,42,time+1, 2,65)
            self.MIDIobj.addNote(0,9,42,time+2, 2,55)
            self.MIDIobj.addNote(0,9,42,time+3, 2,65)

        else:
            # kick
            self.MIDIobj.addNote(0,9,35,time, 2,65)
            self.MIDIobj.addNote(0,9,35,time+1, 2,65)

            # snare
            self.MIDIobj.addNote(0,9,40,time+2, 2,60)

            # hi-hat
            self.MIDIobj.addNote(0,9,42,time, 2,65)
            self.MIDIobj.addNote(0,9,42,time+1, 2,65)
            self.MIDIobj.addNote(0,9,42,time+2, 2,55)
            self.MIDIobj.addNote(0,9,42,time+3, 2,65)


        
    # OTHER METHODS
            
    def get_rhythm(self, possible_rhythms = [1,2], rhythms_weights = [1,1]):
        rhythm_sum = 0
        rhythm = []
        while rhythm_sum != self.quarternotes:
            num = random.choices(possible_rhythms, k=1, weights=rhythms_weights)[0]
            if rhythm_sum + num <= self.quarternotes:
                rhythm_sum += num
                rhythm.append(num)
        return rhythm
    
            
    def midi_to_file(self):
        with open("recording.mid", "wb") as output_file:
            self.MIDIobj.writeFile(output_file)
     