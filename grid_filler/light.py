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
        if stride.dtype != np.dtype('<U1'):
            raise ValueError("Invalid slice data type")
        self._slice = stride
        self.crossers: list[Light] = []

    def __len__(self):
        return len(self.slice)
    
    def __repr__(self):
        return self.slice
    
    @property
    def array(self) -> np.ndarray:
        return self._slice

    @property
    def slice(self) -> str:
        return ''.join(self._slice)

    @slice.setter
    def slice(self, value: str):
        """
        Can also put checks for special characters and
        enusure the letters are upper case here
        """
        if len(value) != len(self):
            raise ValueError(f"Cannot put word of length {len(value)} "
                             f" in a light of length {len(self)}")
        self._slice[:] = list(value)

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