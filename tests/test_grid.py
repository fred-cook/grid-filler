import pytest

from grid_filler.grid import CrosswordGrid


@pytest.fixture
def simple_grid_string():
    return ("### ###"
            "### ###"
            "### ###"
            "       "
            "### ###"
            "### ###"
            "### ###")

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
    
    def test_rectangular_grid(self):
        test_shape = (10, 5)
        test_string = ' ' * test_shape[0] * test_shape[1]
        test_grid = CrosswordGrid(grid_str=test_string,
                                  shape=test_shape)
        assert test_grid.grid.shape == test_shape
        assert len(test_grid.lights) == sum(test_shape)

    def test_simple_grid(self, simple_grid_string):
        test_grid = CrosswordGrid(simple_grid_string,
                                  shape=(7, 7))
        assert len(test_grid.lights) == 2

    def test_incorrect_shape(self):
        """
        If the shape cannot be made exactly from the input string
        """
        with pytest.raises(ValueError):
            _ = CrosswordGrid(' ', (10, 10))