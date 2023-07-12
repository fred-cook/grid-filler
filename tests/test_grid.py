import numpy as np
import pytest

from grid_filler.grid import CrosswordGrid

@pytest.fixture
def example_grid_string():
    return ("#             #"
            " # # # # # # # "
            "       #       "
            " # # # # # # # "
            "     #         "
            " # ##### # ### "
            "     #         "
            " # # # # # # # "
            "         #     "
            " ### # ##### # "
            "         #     "
            " # # # # # # # "
            "       #       "
            " # # # # # # # "
            "#             #")

class TestGrid:
    def test_empty_grid(self):
        """
        An empty grid will have 30 lights (15 across and
        15 down)
        """
        empty_grid = CrosswordGrid(' ' * 225) # 225 == 15**2
        assert len(empty_grid.lights) == 30

    def test_full_grid(self):
        """
        A grid full of blockers will have no lights
        """
        full_grid = CrosswordGrid('#' * 225)
        assert len(full_grid.lights) == 0
    