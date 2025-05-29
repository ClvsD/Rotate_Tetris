import time                          # Para controlar o tempo de queda da peça e movimentos
import pygame                        # Biblioteca principal de jogos
from constants import *              # Importa constantes como GRID_SIZE, COLORS, etc.
from piece import SHAPES, Piece      # Importa os formatos de peças e a classe Piece
import random                        # Para gerar peças aleatórias

class Game:
    def generate_piece(self):
        # Sorteio da peça subsequente
        shape = random.choice(list(SHAPES.keys()))
        return Piece(shape)
    
    def __init__(self):
        # Inicializa o grid do jogo com None (vazio)
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Gera a primeira peça aleatória
        self.current_piece = self.generate_piece()
        
        # Timer para controlar queda automática da peça
        self.drop_timer = time.time()
        
        # Intervalo entre quedas automáticas da peça
        self.drop_interval = 0.3

        # Ponto central do grid (usado na rotação do tabuleiro)
        self.center = (GRID_SIZE // 2 - 1, GRID_SIZE // 2 - 1)

        # Controle do tempo para permitir movimento lateral contínuo
        self.move_timer = 0
        self.move_delay = 0.1

    

    def draw_grid(self, surface):
    # Desenha o grid (células do tabuleiro)
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                color = self.grid[y][x]
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if color:
                    pygame.draw.rect(surface, color, rect)       # Preenche com a cor
                    pygame.draw.rect(surface, BLACK, rect, 1)    # Borda preta opcional
                else:
                    pygame.draw.rect(surface, GRAY, rect, 1) 
    def draw_piece(self, surface):
        # Desenha a peça atual na tela
        for x, y in self.current_piece.get_cells():
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, COLORS[self.current_piece.shape_name], rect)

    def update(self):
        # Atualiza o estado do jogo (queda da peça e colisões)
        now = time.time()
        if now - self.drop_timer > self.drop_interval:
            self.drop_timer = now
            if not self.check_collision(dy=1):
                # Se não colidir, move a peça 1 linha pra baixo
                self.current_piece.position[1] += 1
            else:
                # Se colidir, verifica se há suporte horizontal
                if self.has_horizontal_support():
                    # Fixa a peça no grid
                    for x, y in self.current_piece.get_cells():
                        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                            self.grid[y][x] = COLORS[self.current_piece.shape_name]

                    self.clear_lines()         # Limpa linhas completas
                    self.rotate_board()        # Gira o tabuleiro e ajusta a peça

                    self.current_piece = self.generate_piece()  # Gera nova peça

                    if self.check_collision():
                        # tenta empurrar para baixo
                        pushed = False
                        for i in range(1, 4):
                            self.current_piece.position[1] += 1
                            if not self.check_collision():
                                pushed = True
                                break
                        if not pushed:
                            # Fim de jogo se não há espaço para nova peça
                            print("Game Over")
                            pygame.quit()
                            exit()
                else:
                    # Se não tiver suporte, continua caindo
                    self.current_piece.position[1] += 1

    def handle_held_keys(self, keys):
        # Controla movimento contínuo ao segurar teclas
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
        # Verifica se a peça tem algum suporte horizontal (blocos ao lado na base)
        for x, y in self.current_piece.get_cells():
            below_y = y + 1
            if below_y >= GRID_SIZE:
                return True  # Está no chão
            if self.grid[below_y][x]:
                # Verifica se há blocos ao lado no chão
                if (x > 0 and self.grid[below_y][x - 1]) or (x < GRID_SIZE - 1 and self.grid[below_y][x + 1]):
                    return True
        return False

    def check_collision(self, dx=0, dy=0):
        # Verifica colisão com bordas ou peças já fixadas
        for x, y in self.current_piece.get_cells():
            nx, ny = x + dx, y + dy
            if ny >= GRID_SIZE or nx < 0 or nx >= GRID_SIZE:
                return True  # Fora do grid
            if ny >= 0 and self.grid[ny][nx]:
                return True  # Colidiu com peça fixa
        return False

    def clear_lines(self):
        # Remove linhas completas do grid
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        lines_cleared = GRID_SIZE - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(GRID_SIZE)])  # Insere linhas vazias no topo
        if lines_cleared > 0:
            self.grid = new_grid

    def rotate_board(self):
        # Rotaciona o grid 90° (sentido horário)
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

        # Reposiciona a peça baseada no novo centro rotacionado
        cx, cy = self.center
        new_cells = []
        for x, y in self.current_piece.get_cells():
            # Calcula posição relativa ao centro
            rel_x, rel_y = x - cx, y - cy
            # Aplica rotação (90° sentido horário)
            new_x = cx - rel_y
            new_y = cy + rel_x
            new_cells.append((new_x, new_y))
        self.current_piece.set_cells(new_cells)
