from typing import Tuple, List

import numpy as np
from numpy.lib.stride_tricks import as_strided

from grid_filler.light import Light

class CrosswordGrid:
    """
    Stores an array 
    """
    MIN_LENGTH = 3 # Lights must be at least 3 long
    
    def __init__(self, grid_str: str, shape: Tuple[int, int]=(15, 15)):
        self.grid = self.make_array(grid_str, shape=shape)

        self.across_lights: list[Light]
        self.down_lights: list[Light]
        self.lights = self.extract_lights()
        self.populate_light_crossers()


    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.grid])


    @staticmethod
    def make_array(grid_str: str,
                   shape: Tuple[int, int]=(15, 15)) -> np.ndarray:
        """
        Turn a string into a numpy array

        Parameters
        ----------
        grid_str: str
            A string of characters which represent the grid, ' '
            for lights and '#' for blocked cells. Should have the
            same length as the shape values multipled together
        shape: tuple[int, int]
            The (rows, columns) shape of the output grid

        Returns
        -------
        grid_array: np.ndarray
            
        """
        rows, columns = shape
        if (rows * columns) != len(grid_str):
            raise ValueError("grid_str length doesn't match shape given")
        
        return np.array(list(grid_str)).reshape(*shape)

    def extract_lights(self, white: str=' ') -> List[Light]:
        """
        Return a list of locations and lengths for each light in the
        grid_array

        Parameters
        ----------
        grid_array: np.ndarray
            Grid of characters representing the grid

        Returns
        -------
        light_locations: list[list[int]]
        """
        # convert to array of ones for empty cells, 0 for blocked
        integer_array = np.where(self.grid == white, 1, 0)
        # Find all the across lights
        self.across_lights = [self.create_light(*row)
                  for row in self.get_light_coordinates(integer_array)]
        self.down_lights = [self.create_light(*row, down=True)
                   for row in self.get_light_coordinates(integer_array.T)]
        return self.across_lights + self.down_lights
    
    def populate_light_crossers(self) -> None:
        """
        Given a list of lights, loop over it and store the crossers

        Not as efficient as it could be but only runs once
        """
        for light in self.across_lights:
            light.find_crossers(self.down_lights)
        
        for light in self.down_lights:
            light.find_crossers(self.across_lights)
        

    def create_light(self, row: int, column: int, length: int,
                      down=False) -> Light:
        """
        Given coordinates and a length create a stride_tricks
        view into the grid and save it in a `Light`

        Parameters
        ----------
        light_coordinates: np.ndarray
            
        """
        if down:
            # Switch row and column because coords are calculated transpose
            row, column = column, row
            strides = self.grid.strides[0],
        else:
            strides = self.grid.strides[1],
        light_slice = as_strided(self.grid[row:, column:],
                                     shape=(length,),
                                     strides=strides)
        return Light(light_slice)

    def get_light_coordinates(self, integer_array: np.ndarray) -> np.ndarray:
        """
        Find the start and end point of each row in the array.

        Parameters
        ----------
        integer_array: np.ndarray
            an array with 1s for empty cells and 0s for blocked cells

        Returns
        -------
        coordinate_array: np.ndarray
            an Nx3 array with columns:
                - Row index
                - Column index
                - Length
        """
        # pad the left and right with zeros
        padded = np.pad(integer_array, 1)[1:-1]
        # Take the difference along the rows
        diffed = np.diff(padded, axis=1)
        # Now light starts have value 1 and ends have value -1
        row_indices, starts = np.where(diffed == 1)
        _, ends = np.where(diffed == -1)
        lengths = ends - starts
        # remove any lights which aren't the required length
        return np.c_[row_indices, starts, lengths][lengths >= self.MIN_LENGTH]
