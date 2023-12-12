from pathlib import Path
from collections import defaultdict

import grid_filler as gf
from grid_filler import CrosswordGrid, Light, GridManager

class BasicFiller:
    def __init__(self, theme_path: Path):
        self.grid_manager = GridManager()
        self.theme_dict = self.read_theme(theme_path)

    @staticmethod
    def read_theme(path: Path,
                   min_length: int=3,
                   max_length: int=15) -> defaultdict[int, list[str]]:
        """
        Read the theme from path and convert it into a
        dictionary with word length as the key and a list
        of theme words as the values

        For now the min and max lengths are 3 and 15,
        however a more advanced filler could split words
        across lights
        """
        with open(path) as f:
            theme_words = f.read().split()
        theme_dict = defaultdict(list)
        for word in theme_words:
            if min_length <= (key := len(word)) <= max_length:
                theme_dict[key].append(word)
        return theme_dict


if __name__ == "__main__":
    path = Path(gf.__file__).parent.parent / "themes/languages.txt"
    filler = BasicFiller(path)