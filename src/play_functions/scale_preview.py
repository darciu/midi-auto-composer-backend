from scamp.instruments import ScampInstrument
from scamp import wait
from helper_functions import get_tone_key, create_tonal_scale_and_primes_lists


def play_scale_preview(instrument: ScampInstrument, scale: list, tonal_key: str, min_notes_range: int, max_notes_range: int):
    """
    Play preview of scale on given tonation

    """
    
    tone_key = get_tone_key(tonal_key)

    tonal_scale, _ = create_tonal_scale_and_primes_lists(
        tone_key, scale, min_notes_range, max_notes_range)


    for note_pitch in [elem for elem in tonal_scale if elem <= tonal_scale[0] +24]:

        instrument.play_note(note_pitch, 0.9, 1)

    wait(1)

    instrument.play_note(tonal_scale[0], 0.9, 2)
    
    wait(1)