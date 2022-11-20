import random
import numpy as np




# graj piano, flet, bass osobno
def play_random_notes(instrument, quarternotes, tonal_scale, note_pitch, shift_note_index, move_scale_obj):


    for _ in range(quarternotes):

        instrument.play_note(note_pitch,1,2)

        note_index = tonal_scale.index(note_pitch)

        if shift_note_index == None:
            shift_note_index = np.random.choice(move_scale_obj.move_scale_board, p = move_scale_obj.move_scale_probas)
        else:
            shift_note_index = np.random.choice(move_scale_obj.move_scale_board, p = move_scale_obj.recalculate_probas(shift_note_index))
  
        if (note_index + shift_note_index) < 0:
            shift_note_index = np.random.choice(move_scale_obj.move_scale_board_h2, p = move_scale_obj.move_scale_probas_h2)

        elif (note_index + shift_note_index) > len(tonal_scale)-1:
            shift_note_index = np.random.choice(move_scale_obj.move_scale_board_h1, p = move_scale_obj.move_scale_probas_h1)

        note_pitch = tonal_scale[note_index + shift_note_index]
        
    return note_pitch, shift_note_index


    # zwraca next_note, probas