
import numpy as np
import pytest

from grid_filler.light import Light
from grid_filler.grid import CrosswordGrid

class TestLight:
    def test_initialisation(self):
        LENGTH = 10
        array = np.array(list(" " * LENGTH))
        test_light = Light(array, (0, 0), direction='a')
        assert len(test_light) == LENGTH
        assert test_light.slice == " " * LENGTH

    def test_repr(self):
        word = "ORANGELAD"
        light = Light(np.array(list(word)), coord=(0, 0), direction='a')
        assert str(light) == word

    def test_wrong_datatype(self):
        """
        Not going to test if a non numpy array is passed in
        """
        array = np.ones(10)
        with pytest.raises(ValueError):
            _  = Light(array, (0, 0), direction='a')

    def test_setting_word(self):
        LENGTH = 9
        light = Light(np.array(list(' ' * LENGTH)), (0, 0), 'a')
        assert light.slice == ' ' * LENGTH
        first_word = "ORANGELAD"
        light.slice = first_word
        assert light.slice == first_word
        assert str(light) == first_word
        
        second_word = "CROSSWORD"
        light.slice = second_word
        assert np.all(light._stride == np.array(list(second_word)))

    def test_invalid_word(self):
        light = Light(np.array(list(' ' * 5)), (0, 0), 'a')
        with pytest.raises(ValueError):
            light.slice = "TOOLONG"

    def test_memory_maintained(self, simple_grid_string):
        """
        Test that it is the same section of a NumPy array
        which is changed when a word is entered.
        """
        grid_size = int(len(simple_grid_string)**0.5)
        shape = (grid_size, grid_size)
        grid = CrosswordGrid(simple_grid_string, shape)
        light_1, light_2 = grid.lights
        light_1.slice = "ORANGES"
        assert light_1.shares_memory(light_2)
        light_2.slice = "GRANITE"
        assert light_2.shares_memory(light_1)

