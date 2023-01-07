from scamp import Session

from play_functions.scale_with_pattern import play_scale_with_pattern_upwards, play_scale_with_pattern_downwards


def play_pattern(playback_tempo: int, scale: list, scale_tonation: str, pattern: list, notes_range: tuple, play_upwards: bool):

    sess = Session(tempo=playback_tempo)

    instrument_solo = sess.new_part('cello')

    if play_upwards:

        play_scale_with_pattern_upwards(instrument_solo, scale, scale_tonation, pattern, notes_range)

    else:

        play_scale_with_pattern_downwards(instrument_solo, scale, scale_tonation, pattern, notes_range)