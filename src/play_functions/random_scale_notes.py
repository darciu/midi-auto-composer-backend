
import numpy as np
import scamp
from typing import Optional, Tuple


from src.entities.move_scale import MoveScale



def play_list_of_notes(instrument: scamp.instruments.ScampInstrument, list_of_notes: list) -> None:

    for note_pitch in list_of_notes:

        instrument.play_note(note_pitch,1,2)

def random_notes(quarternotes: int, tonal_scale: list, note_pitch: int, shift_note_index: Optional[int], move_scale_obj: MoveScale) -> Tuple[list, int]:

    list_of_notes = []

    for _ in range(quarternotes):

        note_index = tonal_scale.index(note_pitch)

        if shift_note_index == None:
            shift_note_index = np.random.choice(
                move_scale_obj.move_scale_board, p=move_scale_obj.move_scale_probas)
        else:
            shift_note_index = np.random.choice(
                move_scale_obj.move_scale_board, p=move_scale_obj.recalculate_probas(shift_note_index))

        if (note_index + shift_note_index) < 0:
            shift_note_index = np.random.choice(
                move_scale_obj.move_scale_board_h2, p=move_scale_obj.move_scale_probas_h2)

        elif (note_index + shift_note_index) > len(tonal_scale)-1:
            shift_note_index = np.random.choice(
                move_scale_obj.move_scale_board_h1, p=move_scale_obj.move_scale_probas_h1)

        note_pitch = tonal_scale[note_index + shift_note_index]

        list_of_notes.append(note_pitch)

    return list_of_notes, shift_note_index