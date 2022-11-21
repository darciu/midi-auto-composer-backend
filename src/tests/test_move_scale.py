import sys
import os
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from entities.move_scale import MoveScale

move_scale_obj = MoveScale(4)

def test_normalize_array():
    assert move_scale_obj.normalize_array([1,2,25,6]).sum() == 1
    assert move_scale_obj.normalize_array([556,1234]).sum() == 1
    assert move_scale_obj.normalize_array([9,99,999]).sum() == 1

def test_recalculate_probas():
    assert move_scale_obj.recalculate_probas(2).sum() == 1
    assert move_scale_obj.recalculate_probas(-2).sum() == 1

def test_create_move_scale_board():
    assert move_scale_obj.move_scale_board == [-4,-3,-2,-1,1,2,3,4]

def test_create_move_scale_probas():
    assert move_scale_obj.move_scale_probas.sum() == 1