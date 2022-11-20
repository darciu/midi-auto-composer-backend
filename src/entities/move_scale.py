from dataclasses import dataclass, field
from typing import Literal, Union
import numpy as np


@dataclass
class MoveScale:
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


    def normalize_array(self, values: Union[list,np.array]) -> np.array:
        """normalize array so it sums up to 1"""
        values = np.array(values)
        arr = values / values.min()
        return arr/ arr.sum()


    def __create_move_scale_board(self) -> list:
        move_scale_board = list(range(-self.move_scale_max,self.move_scale_max+1))
        move_scale_board.remove(0)
        return move_scale_board

    def __create_move_scale_probas_easy(self):
        return self.normalize_array(list(range(1,self.move_scale_max+1)) + list(range(1,self.move_scale_max+1))[::-1])

    def __create_move_scale_probas_normal(self):
        return self.normalize_array(np.ones(self.move_scale_max*2))

    def __create_move_scale_probas_hard(self):
        return self.normalize_array(list(range(1,self.move_scale_max+1))[::-1] + list(range(1,self.move_scale_max+1)))

    def recalculate_probas(self, move: int, division_factor: int = 6): 
        idx = (self.move_scale_board.index(move) + 1) * -1
        changed_scale_probas = self.move_scale_probas.copy()
        changed_scale_probas[idx] = changed_scale_probas[idx]/division_factor
        return self.normalize_array(changed_scale_probas)
    
    