from train_modes.one_scale_one_background_chord import play_one_scale_one_background_chord

from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords

scales = Scales.load_scales()
chords = Chords.load_chords()
scales_chords = ScalesChords.create_object()

notes_range = (40, 81)

playback_tempo = 150


play_one_scale_one_background_chord(playback_tempo, scales.all['ionian'], 'a', chords.all['major'], None, 4, 2, False, True, 10, notes_range)