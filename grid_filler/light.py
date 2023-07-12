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
    """
    def __init__(self, stride: np.ndarray):
        self._slice = stride
        self.crossers: list[Light] = []

    def __len__(self):
        return len(self.slice)

    @property
    def slice(self):
        return self._slice

    @slice.setter
    def slice(self, value):
        """
        Can also put checks for special characters and
        enusure the letters are upper case here
        """
        if len(value) != len(self):
            raise ValueError(f"Cannot put word of length {len(value)} "
                             f" in a light of length {len(self)}")
        self._slice[:] = list(value)
