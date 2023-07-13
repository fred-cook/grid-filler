import pytest

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