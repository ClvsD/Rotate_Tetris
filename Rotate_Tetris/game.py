# game.py
import time
import pygame
from constants import *
from piece import SHAPES, Piece
import random

class Game:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_piece = self.generate_piece()
        self.drop_timer = time.time()
        self.drop_interval = 0.3
        self.center = (GRID_SIZE // 2 - 1, GRID_SIZE // 2 - 1)
        self.move_timer = 0
        self.move_delay = 0.1

    def generate_piece(self):
        shape = random.choice(list(SHAPES.keys()))
        return Piece(shape)

    def draw_grid(self, surface):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                color = self.grid[y][x] or GRAY
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, color, rect, 1)



    def draw_piece(self, surface):
        for x, y in self.current_piece.get_cells():
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, COLORS[self.current_piece.shape_name], rect)

    def update(self):
     now = time.time()
     if now - self.drop_timer > self.drop_interval:
        self.drop_timer = now
        if not self.check_collision(dy=1):
            self.current_piece.position[1] += 1
        else:
            # Só trava se houver "base horizontal"
            if self.has_horizontal_support():
                for x, y in self.current_piece.get_cells():
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        self.grid[y][x] = COLORS[self.current_piece.shape_name]
                self.current_piece = self.generate_piece()
                self.rotate_board()
            else:
                self.current_piece.position[1] += 1  # deixa cair mais um pouco

    def handle_held_keys(self, keys):
        now = time.time()
        if now - self.move_timer > self.move_delay:
            if keys[pygame.K_LEFT]:
                if not self.check_collision(dx=-1):
                    self.current_piece.position[0] -= 1
            elif keys[pygame.K_RIGHT]:
                if not self.check_collision(dx=1):
                    self.current_piece.position[0] += 1
            elif keys[pygame.K_DOWN]:
                if not self.check_collision(dy=1):
                    self.current_piece.position[1] += 1
            self.move_timer = now

    def has_horizontal_support(self):
        for x, y in self.current_piece.get_cells():
            below_y = y + 1
            if below_y >= GRID_SIZE:
                return True  # chão
            if self.grid[below_y][x]:
                # verificar se a peça abaixo é parte de uma "base"
                # olhamos se há blocos adjacentes na horizontal
                if (x > 0 and self.grid[below_y][x - 1]) or (x < GRID_SIZE - 1 and self.grid[below_y][x + 1]):
                    return True
        return False

    def check_collision(self, dx=0, dy=0):
        for x, y in self.current_piece.get_cells():
            nx, ny = x + dx, y + dy
            if ny >= GRID_SIZE or nx < 0 or nx >= GRID_SIZE:
                return True
            if ny >= 0 and self.grid[ny][nx]:
                return True
        return False
    
    def rotate_board(self):
        self.grid = [list(row) for row in zip(*self.grid[::-1])]
