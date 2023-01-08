from scamp import Session

from play_functions.simul_scale_chord import play_multiple_scales_chords


def play_multiple_scales_multiple_chords(playback_tempo: int, measures: list, move_scale_max: int, repeat_n_times: int, timeout: int, notes_range: tuple):


    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    instrument_back = sess.new_part('piano')

    instruments = instrument_solo, instrument_back


    sess.start_transcribing()

    play_multiple_scales_chords(sess, instruments, measures, move_scale_max, repeat_n_times, timeout, notes_range)

    midi_obj = sess.stop_transcribing().get_midi_object(playback_tempo, 200)

    return midi_obj