from pathlib import Path

import grid_filler as gf # for __file__ access

class GridManager:
    def __init__(self):
        self.raw_grids = self.get_raw_grids()
        self.grids = [gf.CrosswordGrid(raw) for raw in self.raw_grids]
        
    def get_raw_grids(self) -> list[str]:
        path = Path(gf.__file__).parent.parent / "assets/raw_grids.txt"
        with open(path) as f:
            raw_grids = f.read().split('\n')
        return [raw for raw in raw_grids if raw != '']
