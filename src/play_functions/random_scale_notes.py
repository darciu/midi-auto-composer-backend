import scamp
from typing import Optional, Tuple


from src.entities.move_scale import MoveScale


def play_list_of_notes(instrument: scamp.instruments.ScampInstrument, list_of_notes: list) -> None:

    for note_pitch in list_of_notes:

        if note_pitch < 50:
            instrument.play_note(note_pitch, 1, 2)
        elif note_pitch < 65:
            instrument.play_note(note_pitch, 0.9, 2)
        else:
            instrument.play_note(note_pitch, 0.8, 2)


def find_random_notes(quarternotes: int, tonal_scale: list, note_pitch: int, shift_note_index: Optional[int], move_scale_obj: MoveScale) -> Tuple[list, int]:

    list_of_notes = []

    for _ in range(quarternotes):

        note_pitch, shift_note_index = move_scale_obj.find_new_note(
            shift_note_index, tonal_scale, note_pitch)

        list_of_notes.append(note_pitch)

    return list_of_notes, shift_note_index
