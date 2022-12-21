import random

from scamp import Session

# python -m src.play_modes.random_scale_chord_background

from play_functions.scale_preview import play_scale_preview
from play_functions.simul_scale_chord import play_multiple_scale_chord

from ..entities.scales import Scales
from ..entities.chords import Chords
from ..entities.scales_chords import ScalesChords

scales = Scales.load_scales()
chords = Chords.load_chords()
scales_chords = ScalesChords.create_object()



# from midiutil import MIDIFile


# def get_midi_object(self, playback_tempo: int, midi_tempo: int, max_channels: int = 16,
#                             ring_time: float = 0.5,  pitch_bend_range: float = 2, envelope_precision: float = 0.01) -> MIDIFile:
#     midi_obj = MIDIFile(len(self.parts))
    
#     self.remap_to_tempo(playback_tempo)
#     midi_obj.addTempo(0, 0, midi_tempo)

#     for i, part in enumerate(self.parts):
#         part.write_to_midi_file_track(midi_obj, i, max_channels=max_channels, ring_time=ring_time,
#                                         pitch_bend_range=pitch_bend_range, envelope_precision=envelope_precision)

#     output_file = 'song.mid'
#     #### return output_file
#     if hasattr(output_file, 'write'):
#         midi_obj.writeFile(output_file)
#     else:
#         with open(output_file, "wb") as output_file:
#             midi_obj.writeFile(output_file)
#     return midi_obj


# setattr(scamp.Performance, 'get_midi_object', get_midi_object)



# dla chromatycznej wyłączyć background chords

def interface(scale_preview: bool):

    # quarternotes, scale, chord, key
    # measures = [(4, scales.all['pentatonic_minor'], chords.chords['minor'],'e'),
    #             (4, scales.all['pentatonic_major'], chords.chords['m7'], 'e')]


    measures = [(4, scales.all['pentatonic_minor'], chords.chords['minor'],'e'),
                (4, scales.all['pentatonic_minor'], chords.chords['dominant7'], 'f')]
    

    # params:
    min_notes_range = 40
    max_notes_range = 81

    playback_tempo = 80
    # midi_tempo = 120

    sess = Session(tempo=playback_tempo)

    instrument = sess.new_part('cello')
    instrument_back = sess.new_part('piano')



    move_scale_max = 2

    # sess.start_transcribing()

    if scale_preview:
        play_scale_preview(instrument, scales.all['ionian'],'a', min_notes_range, max_notes_range)

    play_multiple_scale_chord(sess, instrument, instrument_back, measures,
                        move_scale_max, 20, min_notes_range, max_notes_range)

    # sess.stop_transcribing().get_midi_object(playback_tempo, midi_tempo)








interface(scale_preview=False)

