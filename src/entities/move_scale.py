from dataclasses import dataclass, field
from typing import Literal, Union, Tuple
import numpy as np


@dataclass
class MoveScale:
    """A class containing probability board (list) used while choosing new random note.
        There are three types of difficulty:
        - easy: it is more probable to choose new note nearer than farther from actually playing note;
        - normal: probability of choosing near and far notes is uniform;
        - hard: farther notes are more likely to choose

    Attributes
    ----------
    move_scale_max: int
        how distant scale steps are allowed while choosing new note (upwards and downwards moves)
    move_scale_board: list
        initial array with possible moves on scale which looks like this: [1,2,3,3,2,1]
        these numbers will be normalized (probas)
    move_scale_probas: list
        normalized (and while using modified) array with probabilites of moving through the scale

    h1 and h2 are halves of before mentiones arrays
    """
    move_scale_max: int
    difficulty: Literal['easy','normal','hard'] = 'normal'
    move_scale_board: list = field(init=False)
    move_scale_board_h1: list = field(init=False)
    move_scale_board_h2: list = field(init=False)
    move_scale_probas: list = field(init=False)
    move_scale_probas_h1: list = field(init=False)
    move_scale_probas_h2: list = field(init=False)

    def __post_init__(self):
        
        self.move_scale_board = self.__create_move_scale_board()
        
        if self.difficulty == 'easy':
            self.move_scale_probas = self.__create_move_scale_probas_easy()
        elif self.difficulty == 'normal':
            self.move_scale_probas = self.__create_move_scale_probas_normal()
        elif self.difficulty == 'hard':
            self.move_scale_probas = self.__create_move_scale_probas_hard()

        
        self.move_scale_board_h1 = np.array_split(self.move_scale_board,2)[0]
        self.move_scale_board_h2 = np.array_split(self.move_scale_board,2)[1]

        self.move_scale_probas_h1 = self.normalize_array(np.array_split(self.move_scale_probas,2)[0])
        self.move_scale_probas_h2 = self.normalize_array(np.array_split(self.move_scale_probas,2)[1])


    def normalize_array(self, values_list: Union[list,np.array]) -> np.array:
        """Normalize array so it sums up to 1
        
        :param values_list: sequence of values to be normalized
        :type values_list: Union[list, np.array]
        :return: Numpy's array that sums up to 1
        """
        values_array = np.array(values_list)
        arr = values_array / values_array.min()
        return arr/ arr.sum()


    def __create_move_scale_board(self) -> list:
        move_scale_board = list(range(-self.move_scale_max,self.move_scale_max+1))
        move_scale_board.remove(0)
        return move_scale_board

    def __create_move_scale_probas_easy(self) -> np.array:
        return self.normalize_array(list(range(1,self.move_scale_max+1)) + list(range(1,self.move_scale_max+1))[::-1])

    def __create_move_scale_probas_normal(self) -> np.array:
        return self.normalize_array(np.ones(self.move_scale_max*2))

    def __create_move_scale_probas_hard(self) -> np.array:
        return self.normalize_array(list(range(1,self.move_scale_max+1))[::-1] + list(range(1,self.move_scale_max+1)))

    def recalculate_probas(self, move: int, division_factor: int = 6) -> np.array: 
        idx = (self.move_scale_board.index(move) + 1) * -1
        changed_scale_probas = self.move_scale_probas.copy()
        changed_scale_probas[idx] = changed_scale_probas[idx]/division_factor
        return self.normalize_array(changed_scale_probas)
    
    def find_new_note(self, prev_shift_note_index: int, tonal_scale: list, current_note_pitch: int) -> Tuple[int, int]:
        """Find new note pitch according to previous note pitch and tonal scale with certain probabilities
        
        :param prev_shift_note_index: what was the last move on the tonal scale; this helps to prevent loops while playing
        :type prev_shift_note_index: int
        :param tonal_scale: list containing all notes pitches of playing tonal scale
        :type tonal_scale: list
        :param current_note_pitch: actually played note
        :type current_note_pitch: int
        """

        note_index = tonal_scale.index(current_note_pitch)

        if prev_shift_note_index == None:
            shift_note_index = np.random.choice(
                self.move_scale_board, p=self.move_scale_probas)
        else:
            shift_note_index = np.random.choice(
                self.move_scale_board, p = self.recalculate_probas(prev_shift_note_index))


        if (note_index + shift_note_index) < 0:
            shift_note_index = np.random.choice(
                self.move_scale_board_h2, p = self.move_scale_probas_h2)

        elif (note_index + shift_note_index) > len(tonal_scale)-1:
            shift_note_index = np.random.choice(
                self.move_scale_board_h1, p = self.move_scale_probas_h1)

        new_note_pitch = tonal_scale[note_index + shift_note_index]

        return new_note_pitch, shift_note_index
    