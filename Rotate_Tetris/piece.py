# piece.py
import random
from constants import GRID_SIZE

SHAPES = {
    'I': [[(0, 1), (1, 1), (2, 1), (3, 1)]],
    'O': [[(1, 0), (2, 0), (1, 1), (2, 1)]],
    'T': [[(1, 0), (0, 1), (1, 1), (2, 1)]],
    'S': [[(1, 1), (2, 1), (0, 2), (1, 2)]],
    'Z': [[(0, 1), (1, 1), (1, 2), (2, 2)]],
    'J': [[(0, 0), (0, 1), (1, 1), (2, 1)]],
    'L': [[(2, 0), (0, 1), (1, 1), (2, 1)]],
}

class Piece:
    def __init__(self, shape_name):
        self.shape_name = shape_name
        self.blocks = SHAPES[shape_name][0]
        self.position = [GRID_SIZE // 2, 0]  # centro superior da grade

    def get_cells(self):
        return [(x + self.position[0], y + self.position[1]) for x, y in self.blocks]

    def rotate(self):
        # Rotaciona 90° as coordenadas da peça (em relação ao seu próprio centro)
        self.blocks = [(-y, x) for x, y in self.blocks]

    def set_cells(self, cells):
        # Ajusta os blocos com base em coordenadas absolutas
        self.blocks = [(x - self.position[0], y - self.position[1]) for x, y in cells]
