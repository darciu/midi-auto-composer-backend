from scamp.instruments import ScampInstrument


def play_list_of_notes(instrument: ScampInstrument, list_of_notes: list) -> None:

    for note_pitch in list_of_notes:

        # volume adjustment (lower tones are quieter)
        if note_pitch < 50:
            instrument.play_note(note_pitch, 0.9, 2)
        elif note_pitch < 65:
            instrument.play_note(note_pitch, 0.8, 2)
        else:
            instrument.play_note(note_pitch, 0.7, 2)