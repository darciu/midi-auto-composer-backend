import random

from scamp import Session, wait
import scamp

# python -m src.play_modes.random_scale_chord_background

from ..entities.move_scale import MoveScale
from ..entities.scales import Scales
from ..entities.chords import Chords
from ..entities.scales_chords import ScalesChords
from ..play_functions.helper_functions import (
    create_tonal_scale_and_primes_lists, get_tone_key)
from ..play_functions.random_scale_notes import play_list_of_notes, find_random_notes
from ..play_functions.background_chords import play_background_chord

scales = Scales.load_scales()
chords = Chords.load_chords()
scales_chords = ScalesChords.create_object()



from midiutil import MIDIFile


def get_midi_object(self, playback_tempo: int, midi_tempo: int, max_channels: int = 16,
                            ring_time: float = 0.5,  pitch_bend_range: float = 2, envelope_precision: float = 0.01) -> MIDIFile:
    midi_obj = MIDIFile(len(self.parts))
    
    self.remap_to_tempo(playback_tempo)
    midi_obj.addTempo(0, 0, midi_tempo)

    for i, part in enumerate(self.parts):
        part.write_to_midi_file_track(midi_obj, i, max_channels=max_channels, ring_time=ring_time,
                                        pitch_bend_range=pitch_bend_range, envelope_precision=envelope_precision)

    output_file = 'song.mid'
    #### return output_file
    if hasattr(output_file, 'write'):
        midi_obj.writeFile(output_file)
    else:
        with open(output_file, "wb") as output_file:
            midi_obj.writeFile(output_file)
    return midi_obj


setattr(scamp.Performance, 'get_midi_object', get_midi_object)




def interface(play_preview_scale: bool):

    # quarternotes, scale, chord, key
    measures = [(4, scales.all['ionian'], chords.chords['minor'],'e'),
                (4, scales.all['aeolian'], chords.chords['major'], 'g')]

    # measures = [(4, scales.all['pentatonic_minor'], chords.chords['dominant7'],
    #              'g'), (4, scales.all['pentatonic_major'], chords.chords['major'], 'g')]

    # params:
    min_notes_range = 40
    max_notes_range = 81

    playback_tempo = 5000
    midi_tempo = 120

    sess = Session(tempo=playback_tempo)

    instrument = sess.new_part('piano')
    instrument_back = sess.new_part('piano')



    move_scale_max = 3

    sess.start_transcribing()

    if play_preview_scale:
        preview_scale(instrument, scales.all['ionian'],'a', min_notes_range, max_notes_range)

    multiple_scale_chord(sess, instrument, instrument_back, measures,
                        move_scale_max, 10, min_notes_range, max_notes_range)

    sess.stop_transcribing().get_midi_object(playback_tempo, midi_tempo)






def preview_scale(instrument, scale, tonation, min_notes_range, max_notes_range):
    
    tone_key = get_tone_key(tonation)

    tonal_scale, _ = create_tonal_scale_and_primes_lists(
        tone_key, scale, min_notes_range, max_notes_range)



    for note_pitch in [elem for elem in tonal_scale if elem <= tonal_scale[0] +24]:

        instrument.play_note(note_pitch, 0.9, 1)

    wait(1)

    instrument.play_note(tonal_scale[0], 0.9, 2)
    
    wait(1)


def multiple_scale_chord(sess: scamp.Session, instrument: scamp.instruments.ScampInstrument, instrument_back: scamp.instruments.ScampInstrument, measures: list, move_scale_max: int, repeat_n_times: int, min_notes_range: int, max_notes_range: int):

    note_pitch = None
    for _ in range(repeat_n_times):

        for measure in measures:
            note_pitch = single_scale_chord(sess,
                instrument, instrument_back, measure[0], measure[1], measure[2], measure[3], note_pitch, move_scale_max, min_notes_range, max_notes_range)





def single_scale_chord(sess: scamp.Session, instrument: scamp.instruments.ScampInstrument, instrument_back: scamp.instruments.ScampInstrument, quarternotes: 4, scale: list, chord: list, tonation: str, note_pitch: int, move_scale_max: int, min_notes_range: int, max_notes_range: int):

    move_scale_obj = MoveScale(move_scale_max, difficulty='hard')

    tone_key = get_tone_key(tonation)

    tonal_scale, primes = create_tonal_scale_and_primes_lists(
        tone_key, scale, min_notes_range, max_notes_range)

    tonal_chord, _ = create_tonal_scale_and_primes_lists(
        tone_key, chord, min_notes_range, max_notes_range)

    shift_note_index = None

    if note_pitch == None:
        # random first note (prime)
        note_pitch = random.choice(primes)

    elif note_pitch not in tonal_scale:
        note_pitch = min(tonal_scale, key=lambda x: abs(x-note_pitch))

    list_of_notes, shift_note_index = find_random_notes(
        quarternotes, tonal_scale, note_pitch, shift_note_index, move_scale_obj)
    note_pitch = list_of_notes[-1]
    sess.fork(play_list_of_notes, args=[instrument, list_of_notes])
    sess.fork(play_background_chord, args=[
           instrument_back, quarternotes, tonal_chord,0.4])
    sess.wait_for_children_to_finish()

    return note_pitch


interface(play_preview_scale=False)

#---




