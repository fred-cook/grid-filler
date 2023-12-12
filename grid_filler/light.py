from collections import deque
import re

import numpy as np

class Light:
    """
    A light is a location a word can go in the crossword grid

    Each light stores a strided view into the grid array and
    a list of crossing lights

    Attributes
    ----------
    slice: np.ndarray
        A slice of the grid array which contains the light
    crossers: list[Light]
        A list of all the intersecting lights
    cache: deque[re.Pattern]
        Stores previous states of the word for when it gets
        removed
    """
    def __init__(self, stride: np.ndarray):
        if stride.dtype != np.dtype('<U1'):
            raise ValueError("Invalid slice data type")
        self.slice = stride
        self.crossers: list[Light] = []

        self.pattern = re.compile(self.word)
        self.cache: deque[re.Pattern] = deque()

    def __len__(self):
        return len(self.word)
    
    def __repr__(self):
        return self.word

    @property
    def word(self) -> str:
        return ''.join(self.slice)

    def enter_word(self, value: str) -> None:
        """
        Can also put checks for special characters and
        enusure the letters are upper case here
        """
        if len(value) != len(self):
            raise ValueError(f"Cannot put word of length {len(value)} "
                             f" in a light of length {len(self)}")
        self.slice[:] = list(value)
        self.update_pattern()
        for crosser in self.crossers:
            crosser.update_pattern()

    def update_pattern(self) -> None:
        """
        Update the regex pattern stored in self.cache

        If already a complete word don't add to cache
        """
        if '.' in self.pattern.pattern:
            self.cache.append(self.pattern)
        self.pattern = re.compile(self.word)



    def shares_memory(self, other: 'Light') -> bool:
        """
        Check if two slices intersect

        Parameters
        ----------
        other: Light

        Returns
        -------
        bool
            True if the lights overlap in the grid
        """
        if not isinstance(other, self.__class__):
            raise ValueError(f"Must be of type {self.__class__}")
        elif other is self:
            return False
        return np.shares_memory(self._slice, other.array)

    def find_crossers(self, lights: list['Light']) -> None:
        """
        Populate the list of `self.crossers` given a list
        of all the lights in the grid

        This method could be much more efficient, but it's
        only run once and doesn't take long for usual size
        grids
        """
        self.crossers = list(filter(self.shares_memory, lights))