from scamp.instruments import ScampInstrument
from scamp import wait
from .helper_functions import get_tonation, create_tonal_scale_and_primes_lists


def play_scale_preview(instrument_solo: ScampInstrument, scale: list, scale_tonation: str, notes_range: tuple) -> None:
    """
    Play preview of scale on given tonation

    """

    scale_tonation = get_tonation(scale_tonation)

    tonal_scale, _ = create_tonal_scale_and_primes_lists(
        scale, scale_tonation, notes_range)


    for note_pitch in [elem for elem in tonal_scale if elem <= tonal_scale[0] +24]:

        instrument_solo.play_note(note_pitch, 0.9, 1)

    wait(1)

    instrument_solo.play_note(tonal_scale[0], 0.9, 2)
    
    wait(1)