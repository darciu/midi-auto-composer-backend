from train_modes.one_scale_one_chord import play_one_scale_one_chord
from train_modes.pattern import play_pattern
from train_modes.multiple_scales_multiple_chords import play_multiple_scales_multiple_chords
from train_modes.random_background_chords import play_random_background_chords
from train_modes.random_scales_one_chord import play_random_scales_one_chord


from entities.scales import Scales
from entities.chords import Chords
from entities.scales_chords import ScalesChords

scales = Scales.load_scales()
chords = Chords.load_chords()
scales_chords = ScalesChords.create_object()

notes_range = (40, 81)

playback_tempo = 140

# (quarternotes, scale, scale_tonation, chord, chord_tonation)
# 1 mode
# measures = [(4, scales.all['aeolian'], 'a', chords.all['minor'],None)
#             ,(4,scales.all['lydian'],'c',chords.all['major'],None)]
# play_multiple_scales_multiple_chords(playback_tempo, measures, 2, 10, None, notes_range)


# # 2 mode
# play_one_scale_one_chord(playback_tempo, scales.all['ionian'], 'e', chords.all['major'], None, 4, 3, True, True, 15, None, notes_range)


# 3 mode
# play_pattern(playback_tempo, scales.all['wholetone'], 'random', [1,2,3], notes_range, True)



# # 4 mode
# chords = [(chords.all['major'],'a')
#         ,(chords.all['minor'],'c#')
#         ,(chords.all['dominant7'],'e')]
# play_random_background_chords(playback_tempo, chords, 4, 10, 10, notes_range)


# # 5 mode

# scales = [scales.all['pentatonic_minor'], scales.all['pentatonic_major'], scales.all['mixolydian']]

# play_random_scales_one_chord(playback_tempo, scales, 'd', chords.all['dominant7'], None, 15, 4, 2, 10, notes_range)

